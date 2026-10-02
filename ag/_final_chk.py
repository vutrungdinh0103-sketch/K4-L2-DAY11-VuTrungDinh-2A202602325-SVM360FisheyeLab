import csv, io, subprocess, sys

out = []
r = subprocess.run([sys.executable, "lab11.py", "check"], capture_output=True)
out.append("## lab11.py check")
out.append(r.stdout.decode("utf-8", "replace").strip())
out.append(r.stderr.decode("utf-8", "replace").strip())

rows = list(csv.reader(io.open("submission/findings.csv", encoding="utf-8-sig", newline="")))
h, body = rows[0], rows[1:]
ci = {n: i for i, n in enumerate(h)}
out.append("")
out.append("## findings.csv: %d dong" % len(body))
rounds = {}
cells, mcells, zones = set(), set(), set()
for x in body:
    rounds[x[ci["round"]]] = rounds.get(x[ci["round"]], 0) + 1
    cells.add((x[ci["cell"]], x[ci["what"]]))
    if x[ci["cell"]].startswith("M") or "_M" in x[ci["cell"]]:
        mcells.add((x[ci["cell"]], x[ci["what"]]))
    for z in ("center", "mid", "edge"):
        if z in x[ci["evidence"]] or z in x[ci["note"]]:
            zones.add(z)
out.append("round: " + str(rounds))
out.append("cell x what: %d | M-cell x what: %d | zone xuat hien: %s" % (len(cells), len(mcells), sorted(zones)))
acts = {}
for x in body:
    acts[(x[ci["action"]], x[ci["severity"]])] = acts.get((x[ci["action"]], x[ci["severity"]]), 0) + 1
out.append("action x severity: " + str(sorted(acts.items())))
out.append("")
out.append("## Dong r3_diag R4 (sau khi sua)")
for i, x in enumerate(body, 2):
    if x[ci["round"]] == "r3_diag" and x[ci["object_ref"]] == "R4" and x[ci["frame"]] == "adasind_199770.jpg":
        for k in h:
            out.append("  %-14s %s" % (k, x[ci[k]]))
out.append("")
out.append("## 40_decision_log.csv")
out.append(io.open("submission/40_decision_log.csv", encoding="utf-8-sig").read().strip())
out.append("")
out.append("## 45_sampling_plan.csv")
sp = io.open("submission/45_sampling_plan.csv", encoding="utf-8-sig").read().strip()
out.append(sp)
num = []
for line in sp.splitlines()[1:]:
    for part in line.split(",")[1:]:
        p = part.strip()
        if p.isdigit():
            num.append(int(p))
out.append("tong cac so trong dong: %s" % sum(num))

io.open("_final.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote _final.txt")
