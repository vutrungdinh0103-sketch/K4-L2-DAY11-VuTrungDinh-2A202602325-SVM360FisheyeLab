"""Quet submission/: marker con thieu + in noi dung cac file nho."""
from pathlib import Path

base = Path(__file__).resolve().parent
sub = base / "submission"
MARKS = ("TODO", "TBD", "FIXME", "<điền>")
out = []

out.append("### markers")
for path in sorted(sub.rglob("*")):
    if not path.is_file() or path.suffix.lower() not in (".md", ".csv", ".json", ".txt", ".html", ".xml"):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    for number, line in enumerate(text.splitlines(), 1):
        if any(mark in line for mark in MARKS):
            out.append("%s:%d: %s" % (path.relative_to(base).as_posix(), number, line.strip()[:200]))

out.append("")
out.append("### screenshots")
shots = base / "submission" / "screenshots"
out.append(", ".join(p.name for p in sorted(shots.glob("*")) if p.is_file()) or "(rong)")

SMALL = ["submission/00_setup/doctor.txt", "submission/00_setup/mode.json",
         "submission/00_setup/sensor_context.md", "submission/README.md",
         "submission/20_guideline_patch.md", "submission/30_escalation_ticket.md",
         "submission/45_review_plan.md", "submission/46_gold_set_plan.md",
         "submission/50_exit_ticket.md", "submission/40_decision_log.csv",
         "submission/45_sampling_plan.csv", "submission/r1_craft/selfqc.md",
         "submission/r1_craft/reference.txt", "submission/r2_qa/qa_review.md",
         "submission/r3_diag/model_compare.md", "submission/r3_diag/iou_sweep.md",
         "submission/p1_calib/compare.md", "submission/parking/observations.md",
         "submission/r3_diag/local_quality_confusion.csv"]
for name in SMALL:
    path = sub / Path(name).relative_to("submission")
    out.append("")
    out.append("### " + name + " (%s)" % ("co" if path.is_file() else "KHONG CO"))
    if path.is_file():
        out.append(path.read_text(encoding="utf-8").rstrip())

target = base / "_scan.txt"
target.write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote", target)
