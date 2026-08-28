#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

def deploy(target_repo_path: str, new_pkg_name: str):
    target_dir = Path(target_repo_path)
    if not target_dir.exists():
        print(f"Error: {target_dir} does not exist.")
        return

    # Create src package
    src_dir = target_dir / "src" / new_pkg_name
    src_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy files from gtta
    source_src = Path("src/gtta")
    for file in ["__init__.py", "agent.py", "app.py", "cli.py", "db.py", "langchain.py", "llamaindex.py", "mcp_server.py", "server.py"]:
        shutil.copy(source_src / file, src_dir / file)
        
    # Copy dark factory script
    scripts_dir = target_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    shutil.copy("scripts/dark_factory_worker.py", scripts_dir / "dark_factory_worker.py")
    shutil.copy("scripts/optimize_prompt_dspy.py", scripts_dir / "optimize_prompt_dspy.py")

    # Perform find and replace gtta -> new_pkg_name
    for py_file in src_dir.glob("*.py"):
        content = py_file.read_text()
        content = content.replace("gtta", new_pkg_name)
        content = content.replace("Global Think Tank Analyst", new_pkg_name.upper())
        py_file.write_text(content)
        
    for py_file in scripts_dir.glob("*.py"):
        content = py_file.read_text()
        content = content.replace("gtta", new_pkg_name)
        content = content.replace("Global Think Tank Analyst", new_pkg_name.upper())
        py_file.write_text(content)

    # Update pyproject.toml
    pyproj = target_dir / "pyproject.toml"
    if pyproj.exists():
        content = pyproj.read_text()
        if "[project.scripts]" not in content:
            content += f"\n\n[project.scripts]\n{new_pkg_name} = \"{new_pkg_name}.cli:app\"\n"
        if "[project.optional-dependencies]" not in content:
            content += """
[project.optional-dependencies]
docs = ["mkdocs-material"]
eval = ["promptfoo"]
ui = ["streamlit>=1.30.0"]
agent = ["langchain-openai", "langchain-anthropic", "langchain-community", "duckduckgo-search", "tavily-python", "langgraph", "networkx"]
test = ["pytest>=7.0.0", "pytest-asyncio"]
dspy = ["dspy-ai"]
enterprise = ["fastapi", "uvicorn", "pypdf", "faiss-cpu", "langchain-huggingface"]
"""
        pyproj.write_text(content)
    
    print(f"Successfully deployed Dark Factory engine to {new_pkg_name} in {target_repo_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: deploy_engine_to_vertical.py <target_path> <new_package_name>")
        sys.exit(1)
    deploy(sys.argv[1], sys.argv[2])
