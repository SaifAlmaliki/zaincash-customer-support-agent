from pypdf import PdfReader

reader = PdfReader("../data/kb-pdf/refund_request.pdf")
page = reader.pages[0]
resources = page["/Resources"]["/Font"].get_object()
for name, font in resources.items():
    font = font.get_object()
    print("FONT", name, "subtype", font.get("/Subtype"), "base", font.get("/BaseFont"))
    to_unicode = font.get("/ToUnicode")
    if to_unicode:
        data = to_unicode.get_object().get_data()
        print(data[:1500].decode("latin-1", errors="replace"))
        print("--- end head, len", len(data))
