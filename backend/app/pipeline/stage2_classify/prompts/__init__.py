from pathlib import Path

PROMPT_VERSION = "v1"
_DIR = Path(__file__).parent


def render_prompt(name: str, **values: str) -> str:
    """Fill <<KEY>> markers. `ticket` is always substituted last, so marker-like text inside a ticket is never expanded."""
    text = (_DIR / f"{name}.md").read_text(encoding="utf-8")
    for key in sorted(values, key=lambda k: k == "ticket"):
        text = text.replace(f"<<{key.upper()}>>", values[key])
    return text
