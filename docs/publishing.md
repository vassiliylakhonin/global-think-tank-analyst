# Publishing Python releases

Python distributions are published through GitHub Actions and PyPI Trusted
Publishing. Do not store a PyPI API token in this repository.

## PyPI publisher identity

Configure the following publisher in PyPI. For the first release, use the
pending-publisher form under the account's Publishing settings.

| Field | Value |
|---|---|
| PyPI project | `global-think-tank-analyst` |
| GitHub owner | `vassiliylakhonin` |
| GitHub repository | `global-think-tank-analyst` |
| Workflow | `publish-pypi.yml` |
| GitHub environment | `pypi` |

The identity must match exactly. PyPI will reject an OIDC token issued for a
different repository, workflow filename, or environment.

## Release flow

1. Keep `pyproject.toml` and `gtta.__version__` aligned.
2. Run tests, repository checks, distribution metadata checks, and the
   installed-wheel smoke test.
3. Create an annotated version tag and a GitHub release.
4. Let the release event start `publish-pypi.yml`, or manually dispatch the
   workflow for an existing tag:

   ```bash
   gh workflow run publish-pypi.yml -f tag=v1.6.0rc3
   ```

5. Verify the workflow attestation and the release through the PyPI JSON API
   and a clean `pip install`.

The workflow intentionally separates the unprivileged build job from the OIDC
publish job. Only the publish job receives `id-token: write`. A GitHub
prerelease stops after the verified build; publishing that prerelease to PyPI
requires an explicit manual dispatch. Stable GitHub releases publish
automatically. Published PyPI files and versions are immutable; never rebuild
an already published version.

The build job intentionally installs only the test and MCP extras. Importing
`gtta.agent` is part of that minimal offline gate; the experimental LangChain
and LangGraph stack is loaded only when an `AnalystAgent` is constructed.
