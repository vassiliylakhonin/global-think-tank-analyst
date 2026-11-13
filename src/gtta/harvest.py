"""Explicit HTTPS capture and offline integrity checks, not source verification."""

from __future__ import annotations

import hashlib
import time
import http.client
import ipaddress
import json
import re
import socket
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator

MAX_BYTES = 2_000_000
SOURCE_ID = r"SRC-[0-9]{2,}"


class Capture(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_id: str = Field(pattern=rf"^{SOURCE_ID}$")
    requested_url: str
    final_url: str
    retrieved_at: datetime
    content_type: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")

    @field_validator("retrieved_at")
    @classmethod
    def aware_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("retrieved_at must include a timezone")
        return value


class CaptureBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: str = "gtta.harvest@1.0"
    sources: list[Capture]

    @field_validator("schema_version")
    @classmethod
    def version(cls, value: str) -> str:
        if value != "gtta.harvest@1.0":
            raise ValueError("unsupported harvest schema")
        return value

    @field_validator("sources")
    @classmethod
    def unique_ids(cls, values: list[Capture]) -> list[Capture]:
        if not values or len({s.source_id for s in values}) != len(values):
            raise ValueError("sources must be nonempty with unique source IDs")
        return values


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden += 1
        if tag in {"p", "br", "div", "li", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.hidden:
            self.hidden -= 1
        if tag in {"p", "div", "li"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def _public_address(url: str) -> tuple[str, str, str]:
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.port not in {None, 443}
    ):
        raise ValueError("harvest accepts public HTTPS URLs on port 443 only")
    host = parsed.hostname.encode("idna").decode("ascii")
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    ips = [item[4][0] for item in addresses]
    if not ips or any(not ipaddress.ip_address(ip).is_global for ip in ips):
        raise ValueError("private, reserved, or non-global addresses are not allowed")
    return (
        host,
        ips[0],
        (parsed.path or "/") + ("?" + parsed.query if parsed.query else ""),
    )


def fetch_https(url: str) -> tuple[bytes, str, str]:
    """Pin a validated public IP per hop, preserving TLS hostname verification."""
    deadline = time.monotonic() + 45
    for _ in range(4):
        if time.monotonic() > deadline:
            raise ValueError("capture exceeded 45-second deadline")
        host, address, target = _public_address(url)
        connection = http.client.HTTPSConnection(host, timeout=15)
        raw = socket.create_connection((address, 443), timeout=15)
        try:
            connection.sock = ssl.create_default_context().wrap_socket(
                raw, server_hostname=host
            )
            connection.request(
                "GET",
                target,
                headers={
                    "Host": host,
                    "User-Agent": "GTTA-harvest/1.0",
                    "Accept-Encoding": "identity",
                },
            )
            response = connection.getresponse()
            if response.status in {301, 302, 303, 307, 308}:
                location = response.getheader("Location")
                if not location:
                    raise ValueError("redirect is missing Location")
                url = urljoin(url, location)
                continue
            if response.status != 200:
                raise ValueError(f"source returned HTTP {response.status}")
            if response.getheader("Content-Encoding", "identity") != "identity":
                raise ValueError("compressed content is not supported")
            content_type = response.getheader("Content-Type", "")
            if content_type.split(";", 1)[0].strip().lower() not in {
                "text/plain",
                "text/html",
                "application/xhtml+xml",
            }:
                raise ValueError("only plain text and HTML sources are supported")
            chunks = []
            size = 0
            while size <= MAX_BYTES:
                if time.monotonic() > deadline:
                    raise ValueError("capture exceeded 45-second deadline")
                chunk = response.read1(min(65536, MAX_BYTES + 1 - size))
                if not chunk:
                    break
                chunks.append(chunk)
                size += len(chunk)
            data = b"".join(chunks)
            if len(data) > MAX_BYTES:
                raise ValueError("source exceeds 2 MB capture limit")
            return data, content_type, url
        finally:
            connection.close()
            raw.close()
    raise ValueError("too many redirects")


def extract_text(data: bytes, content_type: str) -> str:
    charset = re.search(r"charset\s*=\s*[\"']?([\w-]+)", content_type, re.I)
    text = data.decode(charset.group(1) if charset else "utf-8", errors="strict")
    if content_type.split(";", 1)[0].strip().lower() != "text/plain":
        parser = _Text()
        parser.feed(text)
        text = "\n".join(
            line
            for line in (
                " ".join(line.split()) for line in "".join(parser.parts).splitlines()
            )
            if line
        )
    return text


def harvest(url: str, directory: Path, source_id: str = "SRC-01") -> Capture:
    if not re.fullmatch(SOURCE_ID, source_id):
        raise ValueError("source ID must match SRC-XX (at least two digits)")
    manifest = directory / "sources.json"
    sources = (
        CaptureBundle.model_validate_json(manifest.read_text()).sources
        if manifest.exists()
        else []
    )
    if any(item.source_id == source_id for item in sources):
        raise ValueError("source ID already exists; use a new ID for a new capture")
    data, content_type, final_url = fetch_https(url)
    text = extract_text(data, content_type).encode("utf-8")
    if not text.strip():
        raise ValueError("source has no extractable text")
    capture = Capture(
        source_id=source_id,
        requested_url=url,
        final_url=final_url,
        retrieved_at=datetime.now(timezone.utc),
        content_type=content_type,
        sha256=hashlib.sha256(data).hexdigest(),
        text_sha256=hashlib.sha256(text).hexdigest(),
    )
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in (
        (capture.sha256 + ".raw", data),
        (capture.text_sha256 + ".txt", text),
    ):
        path = directory / name
        if path.is_symlink():
            raise ValueError("snapshot paths must not be symlinks")
        if path.exists() and path.read_bytes() != content:
            raise ValueError("existing content-addressed snapshot is corrupt")
        path.write_bytes(content)
    bundle = CaptureBundle(sources=[*sources, capture])
    temporary = directory / "sources.json.tmp"
    if temporary.is_symlink() or manifest.is_symlink():
        raise ValueError("manifest paths must not be symlinks")
    temporary.write_text(bundle.model_dump_json(indent=2) + "\n", encoding="utf-8")
    temporary.replace(manifest)
    return capture


def load_snapshots(manifest: Path) -> dict[str, str]:
    """Check raw/text hashes and re-derive text so the two files cannot diverge."""
    bundle = CaptureBundle.model_validate_json(manifest.read_text(encoding="utf-8"))
    texts = {}
    for source in bundle.sources:
        values = []
        for digest, suffix in ((source.sha256, ".raw"), (source.text_sha256, ".txt")):
            path = manifest.parent / (digest + suffix)
            if path.is_symlink() or path.stat().st_size > MAX_BYTES:
                raise ValueError("invalid snapshot path or size")
            value = path.read_bytes()
            if hashlib.sha256(value).hexdigest() != digest:
                raise ValueError(f"snapshot hash mismatch: {source.source_id}")
            values.append(value)
        if extract_text(values[0], source.content_type).encode("utf-8") != values[1]:
            raise ValueError(
                f"snapshot text does not match raw capture: {source.source_id}"
            )
        texts[source.source_id] = values[1].decode("utf-8")
    return texts
