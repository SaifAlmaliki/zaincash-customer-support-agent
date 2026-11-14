import unicodedata
from pypdf import PdfReader
from pypdf._text_extraction import get_text_operands
from pypdf.generic._font import Font

page = PdfReader("../data/kb-pdf/refund_request.pdf").pages[0]
resources = page["/Resources"].get_object()
font_dict = resources["/Font"].get_object()
fonts = {name: Font.from_font_resource(font.get_object()) for name, font in font_dict.items()}
state = {"font": None}

def before(operator, operands, cm, tm):
    if operator == b"Tf" and operands:
        state["font"] = fonts.get(operands[0])
    if operator != b"Tj" or not operands or state["font"] is None:
        return
    text_operands, is_str, _widths = get_text_operands(
        operands, cm, tm, state["font"], (0, 90, 180, 270),
    )
    decoded = text_operands if is_str else "".join(
        state["font"].character_map.get(char, char) for char in text_operands
    )
    if decoded and any(unicodedata.combining(ch) for ch in decoded):
        print(f"y={tm[5]:7.2f} x={tm[4]:7.2f} {decoded!r} {[hex(ord(c)) for c in decoded]}")

page.extract_text(visitor_operand_before=before)
