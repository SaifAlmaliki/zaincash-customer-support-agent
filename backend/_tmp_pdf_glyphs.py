import re
from pypdf import PdfReader

reader = PdfReader("../data/kb-pdf/refund_request.pdf")
page = reader.pages[0]
resources = page["/Resources"]["/Font"].get_object()
cmaps = {}
for name, font in resources.items():
    font = font.get_object()
    raw = font["/ToUnicode"].get_object().get_data().decode("latin-1")
    mapping = {}
    for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", raw):
        chars = "".join(chr(int(dst[i:i + 4], 16)) for i in range(0, len(dst), 4))
        mapping[int(src, 16)] = chars
    cmaps[str(name)] = mapping

data = page.get_contents().get_data()
# Operators we care about, as raw bytes.
tokens = re.findall(
    rb"(?P<tm>1 0 0 1 (?P<x>-?\d+\.?\d*) (?P<y>-?\d+\.?\d*) Tm \((?P<glyph>.*?)\) Tj)"
    rb"|(?P<td>(?P<tdx>-?\d+\.?\d*) (?P<tdy>-?\d+\.?\d*) Td .*? \((?P<tdglyph>.*?)\) Tj)",
    data,
)
print("token count", len(tokens))

# Simpler scan: find every Tm/Td followed eventually by Tj on the same snippet.
pattern = re.compile(
    rb"(?:1 0 0 1 (?P<x>-?\d+\.?\d*) (?P<y>-?\d+\.?\d*) Tm|(?P<tdx>-?\d+\.?\d*) (?P<tdy>-?\d+\.?\d*) Td)"
    rb".{0,40}?\((?P<glyph>.*?)\) Tj",
    re.S,
)
font = "/F1"
glyphs = []
for match in pattern.finditer(data):
    x = float(match.group("x") or match.group("tdx"))
    y = float(match.group("y") or match.group("tdy"))
    raw_glyph = match.group("glyph")
    # PDF literal strings use two-byte CIDs for these fonts.
    if len(raw_glyph) == 2:
        cid = int.from_bytes(raw_glyph, "big")
    elif len(raw_glyph) == 1:
        cid = raw_glyph[0]
    else:
        cid = None
    text = cmaps.get(font, {}).get(cid, f"<{raw_glyph.hex()}>") if cid is not None else "?"
    glyphs.append((round(y, 1), x, text, cid))

# Font switches are rare; F2 is only the title. Detect font from nearby Tf by a second pass.
# The title uses F2 and y~796. Body uses F1. Override title font.
lines = {}
for y, x, text, cid in glyphs:
    use = cmaps["/F2"] if y > 780 else cmaps["/F1"]
    if cid is not None and cid in use:
        text = use[cid]
    lines.setdefault(y, []).append((x, text))

for y in sorted(lines, reverse=True):
    parts = [text for _, text in sorted(lines[y], key=lambda item: item[0])]
    print(f"y={y} {''.join(parts)}")
