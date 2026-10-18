import zipfile
from xml.etree import ElementTree as ET

src = "/home/cvzmh_saif/dev/zaincash-support/presentation/SaifAlmaliki_Topic06_FAZAA_Design_Brief.pptx"
z = zipfile.ZipFile(src)
root = ET.fromstring(z.read("ppt/slides/slide5.xml"))
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
for name in ("header", "accent", "eyebrow", "page"):
    for sp in root.iter(f"{P}sp"):
        nv = sp.find(f".//{P}cNvPr")
        if nv is None or nv.attrib.get("name") != name:
            continue
        print("=" * 20, name)
        spPr = sp.find(f"{P}spPr")
        if spPr is not None:
            print(ET.tostring(spPr, encoding="unicode")[:1200])
        if name in ("eyebrow", "page"):
            for rPr in sp.iter(f"{A}rPr"):
                print("RPR", ET.tostring(rPr, encoding="unicode")[:400])
