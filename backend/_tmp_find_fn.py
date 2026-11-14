from pathlib import Path
text = Path("/home/cvzmh_saif/dev/zaincash-support/backend/.venv/lib/python3.12/site-packages/pypdf/_page.py").read_text(encoding="utf-8")
for i, line in enumerate(text.splitlines(), 1):
    if "def extract_text" in line or "TextExtractor" in line or "def _extract" in line:
        print(f"{i}: {line}")
