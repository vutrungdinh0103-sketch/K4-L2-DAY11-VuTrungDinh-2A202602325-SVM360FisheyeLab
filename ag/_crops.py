from pathlib import Path

from PIL import Image

base = Path('.')
specs = [
    ('adasind_167700.jpg', 'a_bike_center', (250, 880, 400, 1200)),
    ('adasind_167700.jpg', 'b_bike_right', (700, 900, 1080, 1400)),
    ('adasind_199770.jpg', 'c_bikes_edge', (40, 760, 240, 960)),
    ('adasind_199770.jpg', 'd_right_ego', (780, 760, 1080, 1400)),
    ('adasind_199770.jpg', 'e_threewheel', (300, 760, 560, 1010)),
    ('adasind_199770.jpg', 'f_peds_center', (540, 780, 730, 1060)),
]
out = base / '_crops'
out.mkdir(exist_ok=True)
lines = []
for name, tag, box in specs:
    image = Image.open(base / 'assets' / 'images' / name).convert('RGB')
    crop = image.crop(box)
    crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
    target = out / ('%s_%s.png' % (name.replace('.jpg', ''), tag))
    crop.save(target)
    lines.append('%s %s %s' % (target.name, image.size, box))
(base / '_crops.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
