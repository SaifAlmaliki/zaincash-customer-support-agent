import unicodedata
from pathlib import Path

from pypdf import PdfReader
from pypdf._text_extraction import get_text_operands
from pypdf.generic._font import Font


def is_rtl(ch: str) -> bool:
    code = ord(ch)
    return 0x0590 <= code <= 0x08FF or 0xFB50 <= code <= 0xFDFF or 0xFE70 <= code <= 0xFEFF


def is_ltr(ch: str) -> bool:
    return ch.isascii() and (ch.isalnum() or ch == "_")


def token_kind(token: str) -> str:
    if any(is_rtl(ch) for ch in token):
        return "rtl"
    if any(is_ltr(ch) for ch in token):
        return "ltr"
    return "neutral"


def visual_tokens_to_logical(tokens: list[str]) -> str:
    tokens = list(reversed(tokens))
    pieces: list[str] = []
    index = 0
    while index < len(tokens):
        if token_kind(tokens[index]) != "ltr":
            pieces.append(tokens[index])
            index += 1
            continue
        end = index + 1
        while end < len(tokens):
            kind = token_kind(tokens[end])
            if kind == "ltr":
                end += 1
                continue
            if kind == "rtl":
                break
            probe = end
            while probe < len(tokens) and token_kind(tokens[probe]) == "neutral":
                probe += 1
            if probe < len(tokens) and token_kind(tokens[probe]) == "ltr":
                end = probe + 1
                continue
            break
        pieces.extend(reversed(tokens[index:end]))
        index = end
    return "".join(pieces)


def extract(page) -> str:
    resources = page["/Resources"].get_object()
    font_dict = resources["/Font"].get_object()
    fonts = {name: Font.from_font_resource(font.get_object()) for name, font in font_dict.items()}
    state = {"font": None}
    glyphs: list[tuple[float, float, int, str]] = []
    seq = 0

    def before(operator, operands, cm, tm):
        nonlocal seq
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
        if decoded:
            glyphs.append((tm[5], tm[4], seq, decoded))
            seq += 1

    page.extract_text(visitor_operand_before=before)
    lines: list[tuple[float, list]] = []
    for y, x, order, text in glyphs:
        for baseline, items in lines:
            if abs(baseline - y) <= 2:
                items.append((x, order, text))
                break
        else:
            lines.append((y, [(x, order, text)]))
    def combining_only(text: str) -> bool:
        return bool(text) and all(unicodedata.combining(ch) for ch in text)

    parts = []
    for _y, items in sorted(lines, key=lambda item: item[0], reverse=True):
        ordered = sorted(items)
        bases: list[tuple[float, int, str]] = []
        marks: list[tuple[float, int, str]] = []
        for x, order, text in ordered:
            (marks if combining_only(text) else bases).append((x, order, text))
        for x, _order, text in marks:
            if not bases:
                continue
            nearest = min(range(len(bases)), key=lambda index: abs(bases[index][0] - x))
            bx, bo, bt = bases[nearest]
            bases[nearest] = (bx, bo, bt + text)
        tokens = [text for _x, _order, text in bases]
        if any(is_rtl(ch) for token in tokens for ch in token):
            parts.append(visual_tokens_to_logical(tokens))
        else:
            parts.append("".join(tokens))
    return "\n".join(parts)


root = Path("../data/kb-pdf")
for name in ("refund_request.pdf", "general_inquiry.pdf"):
    print("=" * 16, name)
    print(extract(PdfReader(str(root / name)).pages[0]))
