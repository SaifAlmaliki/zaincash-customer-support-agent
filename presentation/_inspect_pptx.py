import zipfile
from xml.etree import ElementTree as ET

src = "/home/cvzmh_saif/dev/zaincash-support/presentation/SaifAlmaliki_Topic06_FAZAA_Design_Brief.pptx"
z = zipfile.ZipFile(src)
pres = ET.fromstring(z.read("ppt/presentation.xml"))
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
sldSz = pres.find(f"{P}sldSz")
print("SLIDE SIZE", sldSz.attrib)
sldIdLst = pres.find(f"{P}sldIdLst")
for s in sldIdLst:
    print("sldId", s.attrib)
print("--- SLIDE 5 SHAPES ---")
root = ET.fromstring(z.read("ppt/slides/slide5.xml"))
EMU = 914400


def emu(v):
    return round(int(v) / EMU, 2)


for i, el in enumerate(list(root.iter(f"{P}sp")) + list(root.iter(f"{P}pic")) + list(root.iter(f"{P}cxnSp"))):
    nv = el.find(f".//{P}cNvPr")
    name = nv.attrib.get("name") if nv is not None else "?"
    xfrm = el.find(f".//{A}xfrm")
    texts = []
    for t in el.iter(f"{A}t"):
        if t.text:
            texts.append(t.text)
    pos = ""
    if xfrm is not None:
        off = xfrm.find(f"{A}off")
        ext = xfrm.find(f"{A}ext")
        if off is not None and ext is not None and "cx" in ext.attrib:
            pos = (
                f"x={emu(off.attrib.get('x', 0))} y={emu(off.attrib.get('y', 0))} "
                f"w={emu(ext.attrib['cx'])} h={emu(ext.attrib['cy'])}"
            )
    label = " ".join(texts)[:100]
    print(f"{i:02d} {name:28} {pos:46} {label}")
