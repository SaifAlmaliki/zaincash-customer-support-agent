from pypdf import PdfReader

reader = PdfReader("../data/kb-pdf/refund_request.pdf")
print(reader.pages[0].extract_text(extraction_mode="layout"))
