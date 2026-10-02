"""Trich dong r2_qa trong findings.csv + doc vai bao cao ky thuat."""
from pathlib import Path
import csv

base = Path(__file__).resolve().parent
out = []
with (base / "submission" / "findings.csv").open(encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.DictReader(stream))
out.append("### tong dong: %d" % len(rows))
for name in ("r2_qa", "rework"):
    out.append("")
    out.append("### round=" + name)
    for row in rows:
        if row["round"] == name:
            out.append(" | ".join("%s=%s" % (key, row[key]) for key in
                                  ("frame", "object_ref", "cell", "what", "why", "rule_id", "action", "note")))
for name in ("submission/r3_diag/local_quality.md", "submission/r3_diag/local_quality_conflicts.csv",
             "submission/p1_calib/compare.md"):
    path = base / name
    if path.is_file():
        out.append("")
        out.append("### " + name)
        out.append(path.read_text(encoding="utf-8").rstrip())
(base / "_scan2.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("rows", len(rows))
