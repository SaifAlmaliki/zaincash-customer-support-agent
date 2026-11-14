from pypdf import PdfReader

reader = PdfReader("../data/kb-pdf/refund_request.pdf")
page = reader.pages[0]
items = []


def visitor(text, cm, tm, font_dict, font_size):
    if text and text.strip():
        items.append((round(tm[5], 1), tm[4], text))


page.extract_text(visitor_text=visitor)
lines: dict[float, list] = {}
for y, x, text in items:
    lines.setdefault(y, []).append((x, text))

print("=== x-sorted lines ===")
for y in sorted(lines, reverse=True):
    parts = sorted(lines[y], key=lambda item: item[0])
    print(f"y={y}")
    for x, text in parts:
        print(f"  x={x:7.1f} {text}")
    print("  JOIN:", "".join(text for _, text in parts))
    print()
