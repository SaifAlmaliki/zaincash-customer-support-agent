import pypdf._text_extraction as te
import pypdf._text_extraction._text_extractor as extractor
from pypdf import PdfReader
from pathlib import Path


def append_only(text, cm_matrix, tm_matrix, font_resource, font, text_operands, font_size, rtl_dir, visitor_text):
    for raw_character in text_operands:
        text += font.character_map.get(raw_character, raw_character)
    return text, False, ""


te.get_display_str = append_only
extractor.get_display_str = append_only


def is_rtl(ch: str) -> bool:
    code = ord(ch)
    return (
        0x0590 <= code <= 0x08FF
        or 0xFB50 <= code <= 0xFDFF
        or 0xFE70 <= code <= 0xFEFF
    )


def is_ltr(ch: str) -> bool:
    return ch.isascii() and (ch.isalnum() or ch == "_")


def visual_to_logical(line: str) -> str:
    if not any(is_rtl(ch) for ch in line):
        return line
    chars = list(line[::-1])
    index = 0
    while index < len(chars):
        if not is_ltr(chars[index]):
            index += 1
            continue
        end = index + 1
        while end < len(chars):
            if is_ltr(chars[end]):
                end += 1
                continue
            if is_rtl(chars[end]):
                break
            probe = end
            while probe < len(chars) and not is_ltr(chars[probe]) and not is_rtl(chars[probe]):
                probe += 1
            if probe < len(chars) and is_ltr(chars[probe]):
                end = probe + 1
                continue
            break
        chars[index:end] = reversed(chars[index:end])
        index = end
    return "".join(chars)


root = Path("../data/kb-pdf")
for name in ("refund_request.pdf", "general_inquiry.pdf", "wrong_recipient.pdf", "agent_dispute.pdf"):
    reader = PdfReader(str(root / name))
    print("=" * 20, name)
    visual = reader.pages[0].extract_text() or ""
    logical = "\n".join(visual_to_logical(line) for line in visual.splitlines())
    print(logical)
