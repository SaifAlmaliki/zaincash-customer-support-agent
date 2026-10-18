import zipfile
from xml.etree import ElementTree as ET

src = "/home/cvzmh_saif/dev/zaincash-support/presentation/SaifAlmaliki_Topic06_FAZAA_Design_Brief.pptx"
z = zipfile.ZipFile(src)
root = ET.fromstring(z.read("ppt/slides/slide5.xml"))
# print cSld bg
print(ET.tostring(root, encoding="unicode")[:2500])
