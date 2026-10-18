import zipfile
from xml.etree import ElementTree as ET

src = "/home/cvzmh_saif/dev/zaincash-support/presentation/SaifAlmaliki_Topic06_FAZAA_Design_Brief.pptx"
z = zipfile.ZipFile(src)
root = ET.fromstring(z.read("ppt/slides/slide5.xml"))
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

wanted = {
    "risks",
    "risks-heading",
    "risk-title-0",
    "risk-body-0",
    "week-badge-0",
    "week-date-0",
    "week-title-0",
    "week-body-0",
    "schedule",
    "schedule-heading",
    "repo-band",
    "repo-label",
    "repo-url",
    "title",
    "subtitle",
    "footer",
}
for sp in root.iter(f"{P}sp"):
    nv = sp.find(f".//{P}cNvPr")
    name = nv.attrib.get("name") if nv is not None else "?"
    if name not in wanted:
        continue
    print("=" * 20, name)
    solid = sp.find(f".//{A}solidFill")
    if solid is not None:
        print("FILL", ET.tostring(solid, encoding="unicode")[:400])
    ln = sp.find(f".//{A}ln")
    if ln is not None:
        print("LN", ET.tostring(ln, encoding="unicode")[:300])
    for rPr in list(sp.iter(f"{A}rPr"))[:2]:
        print("RPR", rPr.attrib, ET.tostring(rPr, encoding="unicode")[:500])
    for pPr in list(sp.iter(f"{A}pPr"))[:1]:
        print("PPR", ET.tostring(pPr, encoding="unicode")[:300])
