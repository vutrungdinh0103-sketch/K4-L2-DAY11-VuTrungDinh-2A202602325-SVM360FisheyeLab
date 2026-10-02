"""Audit submission/: file tree + required-file gate + TODO/empty scan."""
from pathlib import Path
import hashlib

base = Path(__file__).resolve().parent
sub = base / "submission"

REQUIRED = [
    "00_setup/doctor.txt", "00_setup/mode.json", "00_setup/sensor_context.md",
    "parking/annotations.xml", "parking/observations.md",
    "p1_calib/annotations.xml", "p1_calib/lock.txt", "p1_calib/reference.txt",
    "p1_calib/compare.md", "p1_calib/compare.html",
    "r1_craft/annotations.xml", "r1_craft/lock.txt", "r1_craft/selfqc.md",
    "r1_craft/reference.txt", "r1_craft/compare.md", "r1_craft/compare.html",
    "r2_qa/qa_review.md", "r2_qa/qa_overlay.html",
    "r3_diag/local_quality.md", "r3_diag/local_quality.json", "r3_diag/local_quality_conflicts.csv",
    "r3_diag/local_quality_confusion.csv",
    "r3_diag/model_compare.md", "r3_diag/model_compare.html",
    "r3_diag/zone_table.md", "rework/annotations-v2.xml", "rework/lock2.txt",
    "rework/delta.md", "findings.csv", "10_error_card.md", "20_guideline_patch.md",
    "30_escalation_ticket.md", "40_decision_log.csv", "45_review_plan.md",
    "45_sampling_plan.csv", "46_gold_set_plan.md",
    "50_exit_ticket.md",
]

out = ["## Cây submission/"]
for path in sorted(sub.rglob("*")):
    if path.is_file():
        data = path.read_bytes()
        flag = []
        if not data.strip():
            flag.append("EMPTY")
        if b"TODO" in data or "điền" in path.read_text(encoding="utf-8", errors="replace"):
            flag.append("TODO/điền")
        out.append("%-62s %7d %s" % (path.relative_to(sub).as_posix(), len(data), ",".join(flag)))

out.append("")
out.append("## Gate bắt buộc")
missing = 0
for relative in REQUIRED:
    path = sub / relative
    if not path.is_file():
        out.append("THIẾU   " + relative)
        missing += 1
    else:
        data = path.read_bytes()
        note = []
        if not data.strip():
            note.append("RỖNG")
        if b"TODO" in data:
            note.append("còn TODO")
        if "điền" in data.decode("utf-8", "replace"):
            note.append("còn chữ điền")
        out.append("%-7s %s %d bytes %s" % ("OK" if not note else "LỖI", relative, len(data), " ".join(note)))
out.append("")
out.append("thiếu %d file" % missing)
(base / "_audit.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("xong")
