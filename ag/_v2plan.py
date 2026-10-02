"""Dump boxes (r1_craft / ref / model) cho 2 frame cua slice B3-dense de thiet ke ban v2."""
from pathlib import Path
import sys

base = Path(__file__).resolve().parent
sys.path.insert(0, str(base))
from svm11.cvat_xml import parse_file, boxes, polygons  # noqa: E402

out = []
mine = parse_file(base / "submission" / "r1_craft" / "annotations.xml")
ref = parse_file(base / "data" / "_ref" / "B3-dense.xml")
mod = parse_file(base / "assets" / "model-yolo26m.xml")


def dump_doc(name, doc, frames):
    out.append("==== %s ====" % name)
    for frame in frames:
        image = doc["images"].get(frame)
        out.append("-- %s size=%s" % (frame, image["size"] if image else None))
        for item in boxes(doc, frame):
            x1, y1, x2, y2 = item["box"]
            out.append("   %s%d %-14s %.1f,%.1f-%.1f,%.1f  w=%.1f h=%.1f  attrs=%s id=%s" % (
                "L" if name == "mine" else ("R" if name == "ref" else "M"),
                item["index"], item["label"], x1, y1, x2, y2, x2 - x1, y2 - y1,
                {k: v for k, v in sorted(item["attrs"].items()) if v == "true"}, item["id"]))
        for item in polygons(doc, frame):
            if item["label"] == "ignore_region":
                out.append("   poly %s n=%d" % (item["attrs"].get("reason", "?"), len(item["points"])))


frames = ["adasind_167700.jpg", "adasind_199770.jpg"]
dump_doc("mine", mine, frames)
dump_doc("ref", ref, frames)
dump_doc("model", mod, frames)

(base / "_v2plan.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote", len(out), "lines")
