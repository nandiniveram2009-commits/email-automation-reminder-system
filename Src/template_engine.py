from pathlib import Path
from typing import Dict, Tuple


def render_email_template(
    templates_dir: Path,
    template_name: str,
    context: Dict[str, str],
) -> Tuple[str, str]:
    """
    Load a template file, inject context variables, and return (subject, body).
    Expected first line format: 'Subject: <your subject>'
    """
    template_path = templates_dir / template_name.strip()
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    raw_text = template_path.read_text(encoding="utf-8")

    # Safely format placeholders; missing keys will raise a clear KeyError
    rendered = raw_text.format(**context)
    lines = rendered.splitlines()

    if not lines or not lines[0].startswith("Subject:"):
        raise ValueError(
            f"Template '{template_name}' must start with 'Subject: <text>'"
        )

    subject = lines[0].replace("Subject:", "", 1).strip()
    body = "\n".join(lines[1:]).lstrip("\n")
    return subject, body