"""Diagnostic dump: boxes per frame for every source document used by the lab."""
from pathlib import Path

from svm11.common import circles, slices
from svm11.cvat_xml import parse_file
from svm11.match import classify
from svm11.report import scoped
from svm11.zones import ignored
from svm11.cvat_xml import polygons

BASE = Path(__file__).resolve().parent
FRAMES = slices(BASE)["B3-dense"]
SOURCES = (
    ("L  r1_craft", "submission/r1_craft/annotations.xml"),
    ("R  reference", "data/_ref/B3-dense.xml"),
    ("Q  qa(data/_qa)", "data/_qa/B3-dense.xml"),
    ("M  model", "assets/model-yolo26m.xml"),
    ("P  prefill", "assets/prefill/B3-dense.xml"),
)

out = []
for name, relative in SOURCES:
    path = BASE / relative
    out.append("######## %s :: %s" % (name, relative))
    if not path.is_file():
        out.append("   (missing)")
        continue
    doc = parse_file(path)
    for frame in FRAMES:
        if frame not in doc["images"]:
            out.append("=== %s : (not in file)" % frame)
            continue
        out.append("=== %s" % frame)
        for item in doc["images"][frame]["shapes"]:
            if item["kind"] == "box":
                x1, y1, x2, y2 = item["box"]
                out.append("   box  %-14s x=%.1f y=%.1f w=%.1f h=%.1f src=%s gid=%s occl=%s attrs=%s"
                           % (item["label"], x1, y1, x2 - x1, y2 - y1, item["source"],
                              item["group_id"], item.get("occluded", "?"), item["attrs"]))
            else:
                out.append("   poly %-14s npoints=%d src=%s points=%s attrs=%s"
                           % (item["label"], len(item["points"]), item["source"],
                              ";".join("%.0f,%.0f" % p for p in item["points"]), item["attrs"]))
        out.append("   --- scoped (in-scope, 1-based index) ---")
        for item in scoped(doc, frame):
            x1, y1, x2, y2 = item["box"]
            out.append("   L%-3d %-14s x=%.1f y=%.1f w=%.1f h=%.1f src=%s"
                       % (item["index"], item["label"], x1, y1, x2 - x1, y2 - y1, item["source"]))

left = parse_file(BASE / "submission/r1_craft/annotations.xml")
ref = parse_file(BASE / "data/_ref/B3-dense.xml")
circle_map = circles(BASE)
out.append("######## classify(r1_craft, ref)")
for frame in FRAMES:
    polys = [p["points"] for p in polygons(ref, frame, "ignore_region")]
    issues = classify(scoped(left, frame), scoped(ref, frame), polys, circle_map[frame],
                      ref["images"][frame]["size"])
    out.append("=== %s" % frame)
    for item in issues:
        a, b = item["left"], item["right"]
        out.append("   %-13s %-12s zone=%-6s L=%s R=%s"
                   % (item["what"], item["object_ref"], item["zone"],
                      a and "%s|%.0f,%.0f,%.0f,%.0f" % (a["label"], a["box"][0], a["box"][1], a["box"][2], a["box"][3]),
                      b and "%s|%.0f,%.0f,%.0f,%.0f" % (b["label"], b["box"][0], b["box"][1], b["box"][2], b["box"][3])))

out.append("######## circles")
for frame in FRAMES:
    out.append("   %s %s" % (frame, circle_map.get(frame)))

(BASE / "_boxes.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("written", len(out), "lines")
