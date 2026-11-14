import pypdf
from pathlib import Path
root = Path(pypdf.__file__).parent
for path in root.rglob("*.py"):
    text = path.read_text(encoding="utf-8", errors="replace")
    if "def extract_text" in text or "visitor_text" in text:
        print(path)
