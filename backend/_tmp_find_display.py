from pathlib import Path
root = Path("/home/cvzmh_saif/dev/zaincash-support/backend/.venv/lib/python3.12/site-packages/pypdf")
for path in root.rglob("*.py"):
    text = path.read_text(encoding="utf-8", errors="replace")
    if "def get_display_str" in text:
        print(path)
