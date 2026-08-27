#!/usr/bin/env python3
"""Auto-sync codex/SKILL.md shared sections from canonical root SKILL.md."""

import re
import sys

DIVERGENT_SECTIONS = {
    "Mode F — Analyst Training",
    "Installation and integration",
}

def build_codex():
    # Read root SKILL.md
    with open("SKILL.md", "r", encoding="utf-8") as f:
        root_lines = f.readlines()
        
    # Read codex/SKILL.md
    with open("codex/SKILL.md", "r", encoding="utf-8") as f:
        codex_lines = f.readlines()
        
    root_sections = {}
    current_section = None
    in_fence = False
    buf = []
    
    # Parse root
    for line in root_lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        m = re.match(r"^(#{2,3}) (.+)$", line.rstrip("\n"))
        if m and not in_fence:
            if current_section is not None:
                root_sections[current_section] = buf
            current_section = m.group(2).strip()
            buf = [line]
        elif current_section is not None:
            buf.append(line)
    if current_section is not None:
        root_sections[current_section] = buf

    # Build new codex
    new_codex = []
    current_codex_section = None
    in_fence = False
    codex_buf = []
    
    for line in codex_lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        m = re.match(r"^(#{2,3}) (.+)$", line.rstrip("\n"))
        
        # Frontmatter / pre-sections
        if m and not in_fence:
            if current_codex_section is None:
                new_codex.extend(codex_buf)
            else:
                # Flush previous section
                if current_codex_section in root_sections and current_codex_section not in DIVERGENT_SECTIONS:
                    new_codex.extend(root_sections[current_codex_section])
                else:
                    new_codex.extend(codex_buf)
            
            current_codex_section = m.group(2).strip()
            codex_buf = [line]
        else:
            codex_buf.append(line)
            
    # Flush last section
    if current_codex_section is not None:
        if current_codex_section in root_sections and current_codex_section not in DIVERGENT_SECTIONS:
            new_codex.extend(root_sections[current_codex_section])
        else:
            new_codex.extend(codex_buf)
    else:
        new_codex.extend(codex_buf)

    with open("codex/SKILL.md", "w", encoding="utf-8") as f:
        f.writelines(new_codex)
    print("codex/SKILL.md successfully auto-synced with canonical SKILL.md.")

if __name__ == "__main__":
    build_codex()
