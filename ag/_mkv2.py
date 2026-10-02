"""Sinh submission/rework/annotations-v2.xml tu ban r1_craft da khoa.

Ban v2 = ban r1_craft sau khi sua 16 finding action=rework:
- bo box nam trong ego_body/lens_border (R09),
- bo box tach doi / box rieng cho nguoi trong phuong tien (R02/R03),
- sua lop Truck -> Car / Bike (R04),
- sua hinh hoc cho khop R9 va bo sung box con thieu (R01).

Chay: py _mkv2.py  -> ghi _v2.xml (nguon de `lab11.py lock rework _v2.xml`)
"""
from pathlib import Path
import re
import sys

base = Path(__file__).resolve().parent
sys.path.insert(0, str(base))
from svm11.common import circles  # noqa: E402
from svm11.cvat_xml import parse_bytes  # noqa: E402
from svm11.match import classify, match_pairs  # noqa: E402
from svm11.report import scoped  # noqa: E402
from svm11.zones import ignored, truncated, zone  # noqa: E402

SOURCE = base / "submission" / "r1_craft" / "annotations.xml"
REFS = base / "data" / "_ref" / "B3-dense.xml"
CIRCLES = circles(base)
old_doc = parse_bytes(SOURCE.read_bytes())
ref_doc = parse_bytes(REFS.read_bytes())


def boxes_of(doc, frame):
    return [dict(item, attrs=dict(item["attrs"])) for item in doc["images"][frame]["shapes"]
            if item["kind"] == "box"]


DROP_167700 = {2, 9}
DROP_199770 = {3, 7, 8, 9, 10, 12}


def plan(frame, items):
    out = []
    for item in items:
        index = item["index"]
        if frame == "adasind_167700.jpg":
            if index in DROP_167700:
                continue
            if index == 4:
                item["box"] = (296.0, 942.0, 346.0, 1112.0)
            if index == 5:
                item["label"] = "Car"
            if index == 11:
                item["box"] = (755.0, 1049.0, 975.0, 1283.0)
        elif frame == "adasind_199770.jpg":
            if index in DROP_199770:
                continue
            if index == 1:
                item["box"] = (539.0, 880.0, 610.0, 997.0)
            if index == 6:
                item["label"] = "Bike"
        out.append(item)
    if frame == "adasind_199770.jpg":
        out.append({"label": "Pedestrian", "box": (847.0, 829.0, 905.0, 947.0), "attrs": {}})
        out.append({"label": "Bike", "box": (109.0, 839.0, 144.0, 882.0),
                    "attrs": {"occluded": "true"}})
    return out


def render(frame, items):
    circle = CIRCLES[frame]
    size = old_doc["images"][frame]["size"]
    lines = []
    for item in items:
        x1, y1, x2, y2 = item["box"]
        occluded = (item.get("attrs", {}).get("occluded") or "false").lower() in ("true", "1")
        edge = "true" if zone(item["box"], circle) == "edge" else "false"
        lines.append('    <box label="%s" source="manual" occluded="0" xtl="%.2f" ytl="%.2f" xbr="%.2f" ybr="%.2f" z_order="0">'
                     % (item["label"], x1, y1, x2, y2))
        lines.append('      <attribute name="occluded">%s</attribute>' % ("true" if occluded else "false"))
        lines.append('      <attribute name="truncated">%s</attribute>'
                     % ("true" if truncated(item["box"], circle, size) else "false"))
        lines.append('      <attribute name="edge_zone">%s</attribute>' % edge)
        lines.append('    </box>')
    return "\n".join(lines)


IMAGE_RE = re.compile(r'(<image [^>]*name="([^"]+)"[^>]*>)(.*?)(</image>)', re.S)
BOX_RE = re.compile(r'\n[ \t]*<box\b.*?</box>', re.S)
text = SOURCE.read_text(encoding="utf-8")
report = []
chunks = []
last = 0
for match in IMAGE_RE.finditer(text):
    frame = match.group(2)
    chunks.append(text[last:match.start()])
    inner = BOX_RE.sub("", match.group(3))
    if frame in CIRCLES:
        items = plan(frame, boxes_of(old_doc, frame))
        inner = inner.rstrip() + "\n" + render(frame, items) + "\n  "
        report.append("%s: %d box -> %d box" % (frame, len(boxes_of(old_doc, frame)), len(items)))
    else:
        report.append("%s: giu nguyen" % frame)
    chunks.append(match.group(1) + inner + match.group(4))
    last = match.end()
chunks.append(text[last:])
target = base / "_v2.xml"
target.write_text("".join(chunks), encoding="utf-8")

# --- tu kiem: parse lai, doi chieu voi reference ---
new_doc = parse_bytes(target.read_bytes())
print("\n".join(report))
print("frames:", sorted(new_doc["images"]))
for frame in sorted(new_doc["images"]):
    refs = scoped(ref_doc, frame)
    polys = [p["points"] for p in ref_doc["images"][frame]["shapes"]
             if p["kind"] == "polygon" and p["label"] == "ignore_region"]
    left = scoped(new_doc, frame)
    active = [item for item in left if not ignored(item["box"], polys)]
    pairs = match_pairs(active, refs)
    issues = classify(left, refs, polys, CIRCLES[frame], new_doc["images"][frame]["size"])
    print("--", frame, "L=%d active=%d matched=%d" % (len(left), len(active), len(pairs)))
    for a, b in pairs:
        print("   L%d ~ R%d %s" % (a["index"], b["index"], b["label"]))
    for issue in issues:
        print("   issue %-13s %s (zone %s)" % (issue["what"], issue["object_ref"], issue["zone"]))
