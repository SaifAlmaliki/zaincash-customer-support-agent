from pypdf import PdfReader

reader = PdfReader("../data/kb-pdf/refund_request.pdf")
page = reader.pages[0]
print("mediabox", page.mediabox)
print("--- extract_text ---")
print(page.extract_text())
print("--- visitor ---")


def visitor(text, cm, tm, font_dict, font_size):
    x = tm[4]
    y = tm[5]
    print(f"x={x:7.1f} y={y:7.1f} size={font_size:5.1f} {text!r}")


page.extract_text(visitor_text=visitor)
