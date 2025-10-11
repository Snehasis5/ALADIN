# generator.py
import json
from pathlib import Path
from shutil import copy2
from llm_client import generate_site_files_via_llm, is_configured as llm_is_configured

def generate_project_from_brief(brief: str, req, project_dir: Path, attachments_dir: Path):
    """
    Fully LLM-driven project generation. No built-in templates.
    The LLM must return `index.html`, optionally `main.js` and `README.md`.
    """
    if not llm_is_configured():
        raise RuntimeError("LLM not configured. Cannot generate project.")

    # Serialize attachments for LLM
    att_list = []
    if attachments_dir.exists():
        for p in attachments_dir.iterdir():
            if p.is_file():
                att_list.append({"name": p.name})

    # Generate site files via LLM
    out = generate_site_files_via_llm(brief, att_list)
    if not out:
        raise RuntimeError("LLM generation failed: no output returned")

    # Ensure project directory exists
    project_dir.mkdir(parents=True, exist_ok=True)

    # Write generated files
    (project_dir / "index.html").write_text(out["index_html"])
    if "main_js" in out:
        (project_dir / "main.js").write_text(out["main_js"])
    # If LLM does not return README, generate minimal one
    readme_content = out.get("readme", f"# {req.task}\n\n{brief}")
    (project_dir / "README.md").write_text(readme_content)

    # Copy attachments to project directory (optional)
    if attachments_dir.exists():
        for p in attachments_dir.iterdir():
            if p.is_file():
                copy2(str(p), str(project_dir / p.name))
