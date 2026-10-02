"""Thong tin anh + polygon + box cho 3 frame cua slice B3-dense."""
from pathlib import Path
from xml.etree import ElementTree as ET

base = Path(__file__).resolve().parent
out = []
for name in ("submission/r1_craft/annotations.xml", "submission/rework/annotations-v2.xml",
             "data/_ref/B3-dense.xml", "assets/model-yolo26m.xml"):
    path = base / name
    root = ET.fromstring(path.read_bytes())
    out.append("### " + name)
    for image in root.findall("image"):
        out.append("image name=%s w=%s h=%s id=%s" % (image.get("name"), image.get("width"),
                                                      image.get("height"), image.get("id")))
        points = []
        for node in image:
            if node.tag == "polygon":
                xs = [float(p.split(",")[0]) for p in node.get("points").split(";") if p]
                ys = [float(p.split(",")[1]) for p in node.get("points").split(";") if p]
                points.append("polygon label=%s reason=%s bbox=(%.0f,%.0f)-(%.0f,%.0f) n=%d"
                              % (node.get("label"),
                                 next((a.text for a in node.findall("attribute") if a.get("name") == "reason"), ""),
                                 min(xs), min(ys), max(xs), max(ys), len(xs)))
            elif node.tag == "box":
                out.append("  box label=%-13s xtl=%.1f ytl=%.1f xbr=%.1f ybr=%.1f source=%s occluded=%s"
                           % (node.get("label"), float(node.get("xtl")), float(node.get("ytl")),
                              float(node.get("xbr")), float(node.get("ybr")), node.get("source"),
                              next((a.text for a in node.findall("attribute") if a.get("name") == "occluded"), "")))
        out.extend("  " + line for line in points)
    out.append("")
(base / "_info.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("ok")
