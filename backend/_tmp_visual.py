import pypdf._text_extraction as te
import pypdf._text_extraction._text_extractor as extractor
from pypdf import PdfReader


def append_only(text, cm_matrix, tm_matrix, font_resource, font, text_operands, font_size, rtl_dir, visitor_text):
    for raw_character in text_operands:
        mapped = font.character_map.get(raw_character, raw_character)
        text += mapped
    return text, False, ""


te.get_display_str = append_only
extractor.get_display_str = append_only

reader = PdfReader("../data/kb-pdf/refund_request.pdf")
print(reader.pages[0].extract_text())
