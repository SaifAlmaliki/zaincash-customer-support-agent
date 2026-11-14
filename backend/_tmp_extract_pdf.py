from pathlib import Path
from pypdf import PdfReader

root = Path("../data/kb-pdf")
for name in ("refund_request.pdf", "general_inquiry.pdf", "wrong_recipient.pdf", "agent_dispute.pdf"):
    reader = PdfReader(str(root / name))
    print("=" * 20, name, "=" * 20)
    for index, page in enumerate(reader.pages, 1):
        print("---PAGE", index, "---")
        print(page.extract_text() or "")
