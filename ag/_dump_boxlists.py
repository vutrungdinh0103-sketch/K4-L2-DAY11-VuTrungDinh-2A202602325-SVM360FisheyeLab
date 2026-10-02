"""Compact box listings per frame for the r1_craft, QA and model documents."""
from pathlib import Path

from svm11.common import circles
from svm11.cvat_xml import parse_file
from svm11.report import scoped
from svm11.zones import zone

BASE = Path(__file__).resolve().parent
FRAMES = ("adasind_145860.jpg", "adasind_167700.jpg", "adasind_199770.jpg")
circle_map = circles(BASE)


def listing(relative, title, path_out):
    doc = parse_file(BASE / relative)
    lines = ["# " + title + " :: " + relative]
    for frame in FRAMES:
        lines.append("== " + frame)
        for item in scoped(doc, frame):
            x1, y1, x2, y2 = item["box"]
            lines.append("  %-4d %-13s %7.1f %7.1f %7.1f %7.1f  %-6s occl=%s trunc=%s src=%s"
                         % (item["index"], item["label"], x1, y1, x2 - x1, y2 - y1,
                            zone(item["box"], circle_map[frame]),
                            item["attrs"].get("occluded", "?"), item["attrs"].get("truncated", "?"),
                            item["source"]))
    (BASE / path_out).write_text("\n".join(lines) + "\n", encoding="utf-8")


listing("submission/r1_craft/annotations.xml", "L r1_craft", "_boxes_L.txt")
listing("data/_ref/B3-dense.xml", "R reference", "_boxes_R.txt")
listing("data/_qa/B3-dense.xml", "Q qa", "_boxes_Q.txt")
listing("assets/model-yolo26m.xml", "M model", "_boxes_M.txt")
print("ok")
