"""Do box cua model-yolo26m.xml + ref cho 2 frame chinh, va kiem tra PIL."""
from pathlib import Path
from xml.etree import ElementTree as ET

base = Path(__file__).resolve().parent
out = []
for name in ("assets/model-yolo26m.xml", "data/_ref/B3-dense.xml"):
    root = ET.fromstring((base / name).read_bytes())
    out.append("### " + name)
    for image in root.findall("image"):
        if image.get("name") not in ("adasind_167700.jpg", "adasind_199770.jpg"):
            continue
        out.append(image.get("name"))
        for node in image:
            if node.tag == "box":
                out.append("  %-13s (%.0f,%.0f)-(%.0f,%.0f)" % (node.get("label"), float(node.get("xtl")),
                                                                float(node.get("ytl")), float(node.get("xbr")),
                                                                float(node.get("ybr"))))
try:
    import PIL
    out.append("PIL " + PIL.__version__)
except Exception as exc:  # noqa: BLE001
    out.append("PIL loi: %s" % exc)
images = base / "assets" / "images"
out.append("images: " + ", ".join(sorted(p.name for p in images.glob("*.jpg")) if images.is_dir() else []))
(base / "_dump3.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("xong")
