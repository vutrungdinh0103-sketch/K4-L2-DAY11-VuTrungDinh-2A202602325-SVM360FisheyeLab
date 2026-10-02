"""In toa do polygon trong export r1_craft de kiem tra hinh dang da ve."""
from pathlib import Path
from xml.etree import ElementTree as ET

base = Path(__file__).resolve().parent
root = ET.fromstring((base / "submission" / "r1_craft" / "annotations.xml").read_bytes())
out = []
for image in root.findall("image"):
    name = image.get("name")
    if name == "adasind_145860.jpg":
        continue
    out.append("### " + name)
    for node in image:
        if node.tag != "polygon":
            continue
        points = [(float(p.split(",")[0]), float(p.split(",")[1])) for p in node.get("points").split(";") if p]
        reason = next((a.text for a in node.findall("attribute") if a.get("name") == "reason"), "")
        out.append("polygon %s reason=%s n=%d" % (node.get("label"), reason, len(points)))
        out.append("  " + " ".join("(%.0f,%.0f)" % pair for pair in points))
(base / "_poly.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("ok")
