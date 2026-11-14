from pypdf import PdfReader

reader = PdfReader("../data/kb-pdf/refund_request.pdf")
page = reader.pages[0]
data = page.get_contents().get_data()
text = data.decode("latin-1", errors="replace")
print(text[:8000])
print("---LEN", len(text))
