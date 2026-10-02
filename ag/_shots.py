"""Sinh 6 anh minh chung trong submission/screenshots/ tu anh goc + box that trong XML.

Moi anh la mot vung crop phong to, ve lai box cua: ban r1_craft (do), reference / ban v2 (xanh la),
model yolo26m (cam) va vung ignore_region ego_body cua reference (xam). Toa do lay dung tu
submission/r1_craft/annotations.xml, data/_ref/B3-dense.xml, assets/model-yolo26m.xml, submission/rework/annotations-v2.xml.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

base = Path(__file__).resolve().parent
shots = base / "submission" / "screenshots"
shots.mkdir(parents=True, exist_ok=True)

try:
    FONT = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
    SMALL = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 17)
except OSError:  # pragma: no cover - may du phong
    FONT = ImageFont.load_default()
    SMALL = FONT

RED, GREEN, ORANGE, GRAY = (220, 30, 30), (0, 150, 0), (230, 120, 0), (90, 90, 90)


def render(job):
    image = Image.open(base / "assets" / "images" / job["frame"]).convert("RGB")
    x0, y0, x1, y1 = job["crop"]
    crop = image.crop((x0, y0, x1, y1))
    scale = job["scale"]
    crop = crop.resize((crop.width * scale, crop.height * scale), Image.LANCZOS)
    crop = Image.blend(crop, Image.new("RGB", crop.size, (255, 255, 255)), 0.25)
    canvas = Image.new("RGB", (crop.width, crop.height + 96), "white")
    canvas.paste(crop, (0, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")
    for kind, coords, color, label in job["draw"]:
        a, b, c, d = [(v - off) * scale for v, off in zip(coords, (x0, y0, x0, y0))]
        if kind == "poly_rect":
            draw.rectangle((a, b, c, d), fill=color + (60,), outline=color, width=3)
        else:
            draw.rectangle((a, b, c, d), outline=color, width=4)
        text_y = max(2, min(crop.height - 24, int(b) - 22))
        draw.text((max(2, int(a) + 4), text_y), label, font=SMALL, fill=(255, 255, 255),
                  stroke_width=3, stroke_fill=color)
    draw.text((6, 6), job["title"], font=FONT, fill=(20, 20, 20), stroke_width=3, stroke_fill="white")
    draw.text((6, crop.height + 8), job["caption"], font=SMALL, fill=(20, 20, 20))
    legend = "do: box ban r1_craft  ·  xanh la: reference / ban v2  ·  cam: model yolo26m  ·  xam: vung don't-care cua reference"
    draw.text((6, crop.height + 38), legend, font=SMALL, fill=(70, 70, 70))
    draw.text((6, crop.height + 66), "Anh tu assets/images/" + job["frame"] + " · minh chung cho findings.csv va decision log",
              font=SMALL, fill=(70, 70, 70))
    path = shots / job["name"]
    canvas.save(path)
    return path, canvas.size


def main():
    for job in JOBS:
        written, size = render(job)
        print("%s %s" % (written.name, size))


JOBS = [
    {
        "frame": "adasind_167700.jpg",
        "crop": (860, 690, 1080, 1450), "scale": 2,
        "name": "adasind_167700_ego_body_right.png",
        "title": "adasind_167700 · vung ego_body phia phai (reference 922-1077 x 747-1443)",
        "caption": "L9 Pedestrian cua ban r1_craft nam tron trong ego_body nen bi tra IGNORE_SCOPE va da bo o ban v2.",
        "draw": [
            ("poly_rect", (922, 747, 1077, 1443), GRAY, "ego_body (reference)"),
            ("box", (917.4, 727.0, 1080.0, 1416.2), RED, "L9 Pedestrian · r1_craft (da bo o v2)"),
            ("box", (910, 727, 1080, 1412), ORANGE, "Pedestrian · model yolo26m (M_only)"),
        ],
    },
    {
        "frame": "adasind_167700.jpg",
        "crop": (700, 930, 1080, 1320), "scale": 2,
        "name": "adasind_167700_bike_trim_755_975.png",
        "title": "adasind_167700 · box xe dap phai (L11/R2)",
        "caption": "L11 ban dau keo den sat mep phai (755-1080) nen cham vung don't-care; v2 thu ve dung 755-975 va R2 khop lai.",
        "draw": [
            ("box", (755.1, 949.7, 1080.0, 1292.6), RED, "L11 Bike · r1_craft (qua rong)"),
            ("box", (755, 1049, 975, 1283), GREEN, "Bike · reference & ban v2"),
        ],
    },
    {
        "frame": "adasind_167700.jpg",
        "crop": (260, 900, 400, 1150), "scale": 3,
        "name": "adasind_167700_bike_geometry_296_346.png",
        "title": "adasind_167700 · box xe dap giua khung (L4/R9)",
        "caption": "L4 lech xuong duoi va phong to hon thuc te; v2 chinh ve 296-346 x 942-1112 va R9 khop.",
        "draw": [
            ("box", (309.5, 980.7, 362.4, 1105.8), RED, "L4 Bike · r1_craft (lech)"),
            ("box", (296, 942, 346, 1112), GREEN, "Bike · reference & ban v2"),
            ("box", (313, 1012, 352, 1112), ORANGE, "Bike · model yolo26m"),
        ],
    },
    {
        "frame": "adasind_199770.jpg",
        "crop": (40, 780, 210, 960), "scale": 4,
        "name": "adasind_199770_left_edge_bikes.png",
        "title": "adasind_199770 · cum hai xe dap ria trai",
        "caption": "L6 bi gan Truck nhung vat co hai banh; v2 doi thanh Bike va bo sung box thu hai trung R6.",
        "draw": [
            ("box", (93.0, 847.5, 117.4, 903.4), RED, "L6 Truck · r1_craft (sai lop)"),
            ("box", (91, 836, 119, 903), GREEN, "Bike · reference R5"),
            ("box", (109, 839, 144, 882), GREEN, "Bike · reference R6 (v2 bo sung)"),
            ("box", (77, 832, 147, 904), ORANGE, "Bike · model yolo26m"),
        ],
    },
    {
        "frame": "adasind_199770.jpg",
        "crop": (880, 700, 1080, 1600), "scale": 2,
        "name": "adasind_199770_ego_body_right.png",
        "title": "adasind_199770 · vung ego_body phia phai (reference 924-1080 x 813-1552)",
        "caption": "Hai box L7 (Pedestrian) va L8 (ThreeWheeler) nam trong ego_body; v2 bo ca hai nen khong con box trong vung don't-care.",
        "draw": [
            ("poly_rect", (924, 813, 1080, 1552), GRAY, "ego_body (reference)"),
            ("box", (954.5, 851.9, 1080.0, 1553.5), RED, "L7 Pedestrian · r1_craft (da bo o v2)"),
            ("box", (925.8, 814.9, 1080.0, 1306.2), RED, "L8 ThreeWheeler · r1_craft (da bo o v2)"),
            ("box", (925, 817, 1080, 1307), ORANGE, "Truck · model yolo26m"),
        ],
    },
    {
        "frame": "adasind_199770.jpg",
        "crop": (330, 770, 570, 990), "scale": 3,
        "name": "adasind_199770_model_car_vs_threewheeler.png",
        "title": "adasind_199770 · model goi xe ba banh la Car",
        "caption": "Reference va ban ve cua nguoi gan deu la ThreeWheeler con model yolo26m tra ve Car => mo escalation cho ai_team (D04).",
        "draw": [
            ("box", (371, 810, 532, 947), GREEN, "ThreeWheeler · reference"),
            ("box", (424.5, 817.0, 529.5, 950.3), RED, "L4 ThreeWheeler · r1_craft"),
            ("box", (373, 809, 530, 947), ORANGE, "Car · model yolo26m (M12)"),
        ],
    },
]

if __name__ == "__main__":
    main()

