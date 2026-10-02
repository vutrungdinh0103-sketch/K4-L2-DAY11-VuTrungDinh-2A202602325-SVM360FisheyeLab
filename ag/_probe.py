import sys
from pathlib import Path

sys.path.insert(0, '.')
from svm11.cvat_xml import parse_file, polygons  # noqa: E402
from svm11.zones import ignored  # noqa: E402

base = Path('.')
ref = parse_file(base / 'data' / '_ref' / 'B3-dense.xml')
cands = {
    'adasind_167700.jpg': [(755, 1049, 975, 1283), (757, 1047, 977, 1285), (917, 727, 1080, 1416),
                           (755, 950, 1080, 1293), (296, 942, 346, 1112)],
    'adasind_199770.jpg': [(847, 829, 905, 947), (935, 990, 1080, 1300), (935, 988, 1082, 1302),
                           (954, 852, 1080, 1553), (926, 815, 1080, 1306), (109, 839, 144, 882)],
}
lines = []
for frame, boxes in cands.items():
    shapes = [(p['attrs'].get('reason'), p['points']) for p in polygons(ref, frame, 'ignore_region')]
    lines.append('== ' + frame)
    for reason, pts in shapes:
        xs = [x for x, _ in pts]
        ys = [y for _, y in pts]
        lines.append('   ignore %s bbox=(%d,%d)-(%d,%d) npoints=%d' % (reason, min(xs), min(ys), max(xs), max(ys), len(pts)))
    polys = [pts for _, pts in shapes]
    for box in boxes:
        lines.append('   cand %s ignored=%s' % (box, ignored(box, polys)))
(base / '_probe.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
