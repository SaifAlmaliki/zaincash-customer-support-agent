import zipfile
from xml.etree import ElementTree as ET

src = "/home/cvzmh_saif/dev/zaincash-support/presentation/SaifAlmaliki_Topic06_FAZAA_Design_Brief.pptx"
z = zipfile.ZipFile(src)
root = ET.fromstring(z.read("ppt/slides/slide5.xml"))
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
EMU = 914400
boxes = []
for sp in root.iter(f"{P}sp"):
    nv = sp.find(f".//{P}cNvPr")
    name = nv.attrib.get("name") if nv is not None else "?"
    xfrm = sp.find(f".//{A}xfrm")
    texts = [t.text for t in sp.iter(f"{A}t") if t.text]
    if xfrm is None:
        continue
    off = xfrm.find(f"{A}off")
    ext = xfrm.find(f"{A}ext")
    if off is None or ext is None or "cx" not in ext.attrib:
        continue
    x = int(off.attrib.get("x", 0)) / EMU
    y = int(off.attrib.get("y", 0)) / EMU
    w = int(ext.attrib["cx"]) / EMU
    h = int(ext.attrib["cy"]) / EMU
    boxes.append((name, x, y, w, h, " ".join(texts)))
    flag = ""
    if x < -0.01 or y < -0.01 or x + w > 17.85 or y + h > 10.05:
        flag = " OUT OF SLIDE"
    print(f"{name:22} x={x:5.2f} y={y:5.2f} w={w:5.2f} h={h:5.2f}{flag}  {' '.join(texts)[:90]}")

print("--- overlaps of text shapes ---")
text_boxes = [b for b in boxes if b[5]]
for i, a in enumerate(text_boxes):
    for b in text_boxes[i + 1 :]:
        ax, ay, aw, ah = a[1], a[2], a[3], a[4]
        bx, by, bw, bh = b[1], b[2], b[3], b[4]
        ix = min(ax + aw, bx + bw) - max(ax, bx)
        iy = min(ay + ah, by + bh) - max(ay, by)
        if ix > 0.05 and iy > 0.05:
            print(f"OVERLAP {ix:.2f}x{iy:.2f}  {a[0]}  <>  {b[0]}")
