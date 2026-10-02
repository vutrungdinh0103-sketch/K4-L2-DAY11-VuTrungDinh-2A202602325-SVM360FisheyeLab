"""Ghi lai findings.csv, 40_decision_log.csv, 45_sampling_plan.csv cho dung gate.

Chay: py _fix_csv.py
"""
from pathlib import Path
import csv
import sys

base = Path(__file__).resolve().parent
sub = base / "submission"
sys.path.insert(0, str(base))

from svm11.findings import HEADER, read_rows, validate_rows  # noqa: E402

V = "v1.0.0"
V2 = "v1.1.0"

FINDINGS = [
    # --- calib (C0) ---
    ("calib", "C0", "adasind_019560.jpg", "L1", "na", "SPURIOUS", "E1_annotator_error", "P2",
     "annotator", "R01", "p1_calib/compare.md · zone=center", "keep_with_reason", V,
     "Box thừa ở lượt căn chỉnh C0; C0 không thuộc slice B3-dense nên không đưa vào rework."),
    ("calib", "C0", "adasind_019560.jpg", "L7+R3", "na", "WRONG_CLASS", "E2_guideline_gap", "P1",
     "guideline", "R04", "p1_calib/compare.md · zone=edge", "keep_with_reason", V,
     "Ranh giới Car/Truck cho xe nhỏ ở rìa vòng kính chưa rõ trong R04; xem 20_guideline_patch.md."),
    # --- r1_craft · adasind_167700 ---
    ("r1_craft", "B3-dense", "adasind_167700.jpg", "L9", "na", "IGNORE_SCOPE", "E1_annotator_error", "P0",
     "annotator", "R09", "screenshots/adasind_167700_right_ego_body.png · probe ignored=True",
     "rework", V, "Box Pedestrian 917-1080 nằm gần trọn trong ego_body và lens_border; phải bỏ hoặc thu về phần nhìn thấy."),
    ("r1_craft", "B3-dense", "adasind_167700.jpg", "L11", "na", "IGNORE_SCOPE", "E1_annotator_error", "P0",
     "annotator", "R09", "screenshots/adasind_167700_bike_below_lens.png · probe ignored=True",
     "rework", V, "Cùng chiếc xe đạp dưới vòng kính với R2; box kéo dài vào ego_body nên thành don't-care và R2 bị báo MISSING."),
    ("r1_craft", "B3-dense", "adasind_167700.jpg", "L2", "na", "SPURIOUS", "E1_annotator_error", "P1",
     "annotator", "R02", "r1_craft/compare.md · zone=mid · IoU với R6 chỉ 0.22",
     "rework", V, "Box ThreeWheeler 161-261 chỉ là phần bên phải của chiếc ba bánh mà L7 đã vẽ trọn 25-214."),
    ("r1_craft", "B3-dense", "adasind_167700.jpg", "L4+R9", "na", "BOX_GEOMETRY", "E1_annotator_error", "P2",
     "annotator", "R02", "screenshots/adasind_167700_bike_center.png · zone=mid",
     "rework", V, "Ghép được với R9 nhưng box thiếu phần trên của xe đạp; sửa về 296,942-346,1112."),
    ("r1_craft", "B3-dense", "adasind_167700.jpg", "L5+R4", "na", "WRONG_CLASS", "E2_guideline_gap", "P1",
     "guideline", "R04", "r1_craft/compare.md · zone=center · L5 Truck vs R4 Car",
     "rework", V, "Van nhỏ chở người ở xa: R04 nói van chở người là Car nhưng thiếu ví dụ biên nên dễ gọi Truck; đã sửa thành Car."),
    ("r1_craft", "B3-dense", "adasind_167700.jpg", "R2", "na", "MISSING", "E1_annotator_error", "P1",
     "annotator", "R01", "screenshots/adasind_167700_bike_below_lens.png · zone=mid",
     "rework", V, "Xe đạp 755-975 dưới vòng kính không có box in-scope; bổ sung bằng cách thu L11 về phần nhìn thấy."),
    # --- r1_craft · adasind_199770 ---
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "L7", "na", "IGNORE_SCOPE", "E1_annotator_error", "P0",
     "annotator", "R09", "screenshots/adasind_199770_right_ego_body.png · probe ignored=True",
     "rework", V, "Box Pedestrian 954-1080 nằm trong ego_body và lens_border nên reference không xác nhận được."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "L8", "na", "IGNORE_SCOPE", "E1_annotator_error", "P0",
     "annotator", "R09", "screenshots/adasind_199770_right_ego_body.png · probe ignored=True",
     "rework", V, "Box ThreeWheeler 925-1080 chồng lên vùng ego_body; vật chính nằm trong vùng don't-care."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "L1+R9", "na", "BOX_GEOMETRY", "E1_annotator_error", "P2",
     "annotator", "R02", "r1_craft/compare.md · zone=center · L1 rộng 127.9 so với R9 rộng 71",
     "rework", V, "Box xe đạp rộng gấp đôi vật thật; tạo một FP cho Bike và kéo precision lớp Bike xuống 0.33."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "L3", "na", "SPURIOUS", "E1_annotator_error", "P1",
     "annotator", "R03", "r1_craft/compare.md · zone=mid · box nằm trọn trong L4/R8",
     "rework", V, "Người trên xe ba bánh đã có box R8; box Pedestrian 350-369 là box riêng thừa theo R03."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "L6+R5", "na", "WRONG_CLASS", "E1_annotator_error", "P1",
     "annotator", "R04", "screenshots/adasind_199770_edge_bikes.png · zone=edge",
     "rework", V, "Cụm hai xe đạp ở rìa trái bị gọi là Truck; sửa thành Bike và bổ sung box cho R6."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "L9", "na", "SPURIOUS", "E1_annotator_error", "P2",
     "annotator", "R02", "r1_craft/compare.md · zone=center · chồng lên L2 và L10",
     "rework", V, "Ba box Pedestrian 611-704 nằm trên cùng một người; reference chỉ có một box R1."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "L10", "na", "SPURIOUS", "E1_annotator_error", "P2",
     "annotator", "R02", "r1_craft/compare.md · zone=center · chồng lên L2 và L9",
     "rework", V, "Box thứ ba của cùng người đó; gộp về box L2 đã khớp R1."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "L12", "na", "SPURIOUS", "E1_annotator_error", "P2",
     "annotator", "R02", "r1_craft/compare.md · zone=center · nằm trong L4/R8",
     "rework", V, "Box ThreeWheeler 373-464 tách đôi chiếc xe ba bánh đã có box L4 khớp R8."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "R3", "na", "MISSING", "E1_annotator_error", "P1",
     "annotator", "R01", "screenshots/adasind_199770_right_ego_body.png · probe ignored=False",
     "rework", V, "Pedestrian 847-905 cao 118 px nằm ngoài vùng ignore nhưng bị bỏ sót; đã bổ sung trong bản v2."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "R4", "na", "MISSING", "E2_guideline_gap", "P2",
     "guideline", "R09", "screenshots/adasind_199770_right_ego_body.png · probe ignored=True",
     "keep_with_reason", V, "R4 nằm hơn nửa diện tích trong ego_body nên theo R09 là don't-care; giữ không vẽ và đề xuất làm rõ ngưỡng."),
    ("r1_craft", "B3-dense", "adasind_199770.jpg", "R6", "na", "MISSING", "E1_annotator_error", "P1",
     "annotator", "R01", "screenshots/adasind_199770_edge_bikes.png · zone=edge",
     "rework", V, "Xe đạp thứ hai 109-144 trong cụm rìa trái bị bỏ sót; đã bổ sung trong bản v2."),
    # --- r2_qa: nguoi soat doc lap tren chinh file duoc giao, why de trong theo luat r2_qa ---
    ("r2_qa", "B3-dense", "adasind_167700.jpg", "L9", "L_only", "ATTRIBUTE", "", "P2",
     "annotator", "R05", "r2_qa/qa_overlay.html · data/_qa/B3-dense.xml box 9",
     "keep_with_reason", V, "R11: attribute là phán đoán; box này truncated=true đúng vì bị vòng kính cắt chứ không bị vật khác che."),
    ("r2_qa", "B3-dense", "adasind_199770.jpg", "L8", "L_only", "IGNORE_SCOPE", "", "P0",
     "annotator", "R09", "r2_qa/qa_overlay.html · data/_qa/B3-dense.xml box 8",
     "rework", V, "Box nằm trong vùng ego_body/lens_border nên người soát không thể xác nhận đúng sai; trả lại người gán để bỏ."),
    ("r2_qa", "B3-dense", "adasind_199770.jpg", "L6", "L_only", "WRONG_CLASS", "", "P1",
     "annotator", "R04", "r2_qa/qa_overlay.html · data/_qa/B3-dense.xml box 6",
     "rework", V, "Vật ở rìa trái có hai bánh nhưng bị gán Truck; nghi sai theo R04 và cần mở ảnh gốc xác nhận."),
    ("r2_qa", "B3-dense", "adasind_199770.jpg", "L3", "L_only", "SPURIOUS", "", "P1",
     "annotator", "R03", "r2_qa/qa_overlay.html · data/_qa/B3-dense.xml box 3",
     "rework", V, "Box Pedestrian nằm trọn trong box ThreeWheeler L4; R03 nói người trong phương tiện khác không có box riêng."),
]

# --- r3_diag: WHY/severity/owner/action cho tung dong do `lab11.py model` sinh ra ---
R3 = [
    ("adasind_167700.jpg", "L7+R6", "LR_noM", "MISSING", "E4_model_domain", "P1", "ai_team", "R04", "edge", "escalate",
     "Model gọi xe ba bánh rìa trái là Truck (M8) nên không ghép được với L7/R6; lỗi mapping lớp của model."),
    ("adasind_167700.jpg", "L6+R7", "LR_noM", "MISSING", "E4_model_domain", "P1", "ai_team", "R01", "center", "escalate",
     "Xe tải nhỏ 467-545 có ở L và R nhưng model không có box nào trong vùng này."),
    ("adasind_167700.jpg", "L2", "L_only", "SPURIOUS", "E1_annotator_error", "P2", "annotator", "R02", "mid", "rework",
     "Box tách đôi chiếc ba bánh của L7; model và reference đều không có box riêng ở đây."),
    ("adasind_167700.jpg", "L4+M5", "LM_noR", "SPURIOUS", "E5_unresolved", "P2", "qa", "R02", "mid", "keep_with_reason",
     "Người và model cùng thấy xe đạp 309-362 nhưng R9 lệch nửa trên; chưa đủ bằng chứng nói ai sai — kiểm tiếp IoU 0.3."),
    ("adasind_167700.jpg", "L5", "L_only", "SPURIOUS", "E2_guideline_gap", "P1", "guideline", "R04", "center", "rework",
     "Sau khi sửa class về Car theo R04 box này ghép được với R4/M4; trước rework nó bị bỏ rơi trong ghép ba chiều."),
    ("adasind_167700.jpg", "R2+M7", "RM_noL", "MISSING", "E1_annotator_error", "P1", "annotator", "R01", "mid", "rework",
     "Người và model đều thấy xe đạp 755-975 nhưng box người vẽ kéo vào ego_body nên bị loại; bản v2 đã thu lại."),
    ("adasind_167700.jpg", "R4+M4", "RM_noL", "MISSING", "E2_guideline_gap", "P1", "guideline", "R04", "center", "rework",
     "Cả R và M gọi Car còn người vẽ Truck; đã sửa thành Car theo R04."),
    ("adasind_167700.jpg", "R9", "R_only", "MISSING", "E1_annotator_error", "P1", "annotator", "R01", "mid", "rework",
     "Xe đạp 296-346 cao 170 px; người ghép được ở lượt L/R nhưng model không có, bản v2 đã chỉnh hình học khớp R9."),
    ("adasind_167700.jpg", "M8", "M_only", "SPURIOUS", "E4_model_domain", "P2", "ai_team", "R04", "mid", "escalate",
     "Box Truck của model trùm lên chiếc ba bánh L7/R6 — sai lớp chứ không phải vật thừa thật."),
    ("adasind_199770.jpg", "L5+R7", "LR_noM", "MISSING", "E4_model_domain", "P1", "ai_team", "R04", "mid", "escalate",
     "Xe tải 211-275 có ở L và R nhưng model gán Car (M6) nên cặp ba chiều gãy."),
    ("adasind_199770.jpg", "L11+R2", "LR_noM", "MISSING", "E4_model_domain", "P1", "ai_team", "R01", "edge", "escalate",
     "Xe ba bánh ở mép trái có ở L và R; model không có box khớp (M4/M8 lệch vùng)."),
    ("adasind_199770.jpg", "L4+R8", "LR_noM", "MISSING", "E4_model_domain", "P1", "ai_team", "R04", "center", "escalate",
     "Model gọi xe ba bánh này là Car (M12) nên không ghép được với L4/R8."),
    ("adasind_199770.jpg", "L1+M3", "LM_noR", "SPURIOUS", "E5_unresolved", "P2", "qa", "R02", "center", "keep_with_reason",
     "Người và model cùng thấy xe đạp 538-666 nhưng reference không có box; cần mở lại ảnh và soát reference trước khi kết luận."),
    ("adasind_199770.jpg", "L3+M9", "LM_noR", "SPURIOUS", "E2_guideline_gap", "P2", "guideline", "R03", "mid", "rework",
     "Người và model cùng vẽ box riêng cho người trong xe ba bánh R8; R03 nói không có box riêng."),
    ("adasind_199770.jpg", "L6", "L_only", "SPURIOUS", "E2_guideline_gap", "P1", "guideline", "R04", "edge", "rework",
     "Cụm hai xe đạp rìa trái bị gọi Truck nên lệch cả L6 lẫn R5/R6; đã sửa thành Bike trong bản v2."),
    ("adasind_199770.jpg", "L9", "L_only", "SPURIOUS", "E1_annotator_error", "P2", "annotator", "R02", "center", "rework",
     "Box trùng thứ hai trên cùng người với L2/L10; model chỉ có một box khớp."),
    ("adasind_199770.jpg", "L10", "L_only", "SPURIOUS", "E1_annotator_error", "P2", "annotator", "R02", "center", "rework",
     "Box trùng thứ ba trên cùng người đó; bản v2 chỉ giữ box L2."),
    ("adasind_199770.jpg", "L12", "L_only", "SPURIOUS", "E1_annotator_error", "P2", "annotator", "R02", "center", "rework",
     "Box tách đôi chiếc xe ba bánh đã có L4/R8; model không có box riêng ở 373-464."),
    ("adasind_199770.jpg", "R3+M10", "RM_noL", "MISSING", "E1_annotator_error", "P1", "annotator", "R01", "mid", "rework",
     "Người đi bộ 847-905 nằm ngoài vùng ignore và cả R lẫn M đều có; bản v2 đã bổ sung box."),
    ("adasind_199770.jpg", "R4", "R_only", "MISSING", "E2_guideline_gap", "P2", "guideline", "R09", "mid", "keep_with_reason",
     "Vật nằm trong ego_body/lens_border nhưng vẫn bị báo thiếu: quy tắc miễn trừ chưa đối xứng giữa phía L và phía R."),
    ("adasind_199770.jpg", "R5", "R_only", "MISSING", "E1_annotator_error", "P1", "annotator", "R01", "edge", "rework",
     "Xe đạp 91-119 ở rìa trái bị gọi Truck; bản v2 sửa lớp và giữ đúng hình học."),
    ("adasind_199770.jpg", "R6", "R_only", "MISSING", "E1_annotator_error", "P1", "annotator", "R01", "edge", "rework",
     "Xe đạp thứ hai 109-144 hoàn toàn bị bỏ sót; đã bổ sung trong bản v2."),
    ("adasind_199770.jpg", "R9", "R_only", "MISSING", "E5_unresolved", "P2", "qa", "R02", "center", "keep_with_reason",
     "Chỉ reference có box 539-610; người vẽ hơi rộng và model bỏ qua — cần mở lại ảnh để chốt ranh giới xe đạp."),
    ("adasind_199770.jpg", "M4", "M_only", "SPURIOUS", "E4_model_domain", "P2", "ai_team", "R01", "edge", "escalate",
     "Box model nằm trong vùng lens_border/ego_body; không có vật tương ứng ở L và R."),
    ("adasind_199770.jpg", "M5", "M_only", "SPURIOUS", "E4_model_domain", "P2", "ai_team", "R04", "edge", "escalate",
     "Model vẽ một box Bike rộng 76-146 trong khi cụm xe đạp thật chỉ 91-144."),
    ("adasind_199770.jpg", "M6", "M_only", "SPURIOUS", "E4_model_domain", "P2", "ai_team", "R04", "mid", "escalate",
     "Model gọi xe tải L5/R7 là Car — sai lớp chứ không phải box thừa."),
    ("adasind_199770.jpg", "M8", "M_only", "SPURIOUS", "E4_model_domain", "P2", "ai_team", "R01", "edge", "escalate",
     "Box model trùm vào vùng lens_border mép trái; không có vật tương ứng."),
    ("adasind_199770.jpg", "M11", "M_only", "SPURIOUS", "E4_model_domain", "P2", "ai_team", "R02", "center", "escalate",
     "Model tách người 611-704 thành nhiều box; reference chỉ có một box R1."),
    ("adasind_199770.jpg", "M12", "M_only", "SPURIOUS", "E4_model_domain", "P2", "ai_team", "R04", "center", "escalate",
     "Box Car của model chính là xe ba bánh R8/L4 — sai lớp theo R04."),
    ("adasind_199770.jpg", "M13", "M_only", "SPURIOUS", "E4_model_domain", "P2", "ai_team", "R02", "center", "escalate",
     "Box Pedestrian thừa trong vùng người đi bộ 611-704 đã có M10/M11."),
]

# --- rework: xac nhan viec da sua trong ban v2 (round=rework, rules_version v1.1.0) ---
REWORK = [
    ("adasind_167700.jpg", "R2", "LRM", "MISSING", "E1_annotator_error", "P1", "annotator", "R01", "mid",
     "Bản v2 thu L11 về đúng xe đạp 755-975 nên R2 và M7 ghép lại được; đóng finding MISSING."),
    ("adasind_199770.jpg", "R6", "LRM", "MISSING", "E1_annotator_error", "P1", "annotator", "R01", "edge",
     "Bổ sung box xe đạp 109-144; cụm hai xe đạp rìa trái không còn missing."),
    ("adasind_199770.jpg", "L6+R5", "LRM", "WRONG_CLASS", "E1_annotator_error", "P1", "annotator", "R04", "edge",
     "Sửa lớp Truck thành Bike theo R04; cặp R5/R6 khớp đúng ở bản v2."),
    ("adasind_167700.jpg", "L9+L11", "LRM", "IGNORE_SCOPE", "E1_annotator_error", "P0", "annotator", "R09", "mid",
     "Bỏ box Pedestrian trong ego_body và thu box xe đạp khỏi lens_border; vùng don't-care không còn box."),
]

for frame, ref, cell, what, why, sev, owner, rule, bin_name, action, note in R3:
    FINDINGS.append(("r3_diag", "B3-dense", frame, ref, cell, what, why, sev, owner, rule,
                     "r3_diag/model_compare.md · zone=" + bin_name, action, V, note))

for frame, ref, cell, what, why, sev, owner, rule, bin_name, note in REWORK:
    FINDINGS.append(("rework", "B3-dense", frame, ref, cell, what, why, sev, owner, rule,
                     "rework/delta.md · zone=" + bin_name, "keep_with_reason", V2, note))


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\r\n")
        writer.writerow(header)
        writer.writerows(rows)
    return path


write_csv(sub / "findings.csv", HEADER, FINDINGS)

DECISION_HEADER = "id,date,question,decision,rationale,status".split(",")
DECISIONS = [
    ("D01", "2026-09-28", "C0 có nằm trong phạm vi rework không?",
     "Chỉ ghi finding cho C0 và giữ nguyên bản đã khóa",
     "C0 là frame căn chỉnh để luyện tool; rework chỉ áp cho slice B3-dense đã khóa nên thay đổi ở C0 không kiểm chứng được bằng lock2.txt",
     "accepted"),
    ("D02", "2026-09-28", "Box nằm trong ego_body/lens_border thì bỏ hay giữ?",
     "Bỏ hoặc thu về phần nhìn thấy rồi khóa lại bản v2",
     "R09 cấm box trong vùng don't-care; probe 10x10 cho thấy L9/L11 (167700) và L7/L8 (199770) nằm hơn nửa diện tích trong vùng này",
     "accepted"),
    ("D03", "2026-09-28", "Cụm hai xe đạp rìa trái ở 199770 gán thế nào?",
     "Sửa L6 từ Truck sang Bike và bổ sung box thứ hai",
     "R04 chỉ cho phương tiện hai bánh là Bike; reference tách R5 và R6 nên cụm này cần hai box thay vì một box Truck",
     "accepted"),
    ("D04", "2026-09-28", "Ai sửa lỗi model gọi sai lớp xe ba bánh?",
     "Mở escalation cho ai_team và không dùng model làm chuẩn",
     "Model yolo26m gọi ThreeWheeler thành Truck (M8 ở 167700) và Car (M12 ở 199770) trên nhiều frame; người gán không sửa được model",
     "escalated"),
    ("D05", "2026-09-28", "Lệch Car/Truck cho van nhỏ ở xa xử lý sao?",
     "Tự sửa thành Car theo R04 và đề xuất bổ sung ví dụ biên vào guideline",
     "Vùng 580-700 ở 167700 mờ; R04 đã nói van chở người là Car nhưng thiếu ví dụ nên hai người gán có thể chọn khác nhau",
     "accepted"),
    ("D06", "2026-09-28", "R4 bị báo MISSING dù nằm trong vùng don't-care",
     "Giữ không vẽ và đề xuất luật rõ ngưỡng 50% cho cả hai phía",
     "Probe trả về ignored=True cho R4 nhưng matcher chỉ miễn trừ phía L; vẽ thêm box ở đây sẽ vi phạm R09",
     "escalated"),
    ("D07", "2026-09-28", "Dùng ngưỡng IoU nào để đọc chất lượng cục bộ?",
     "Đọc bảng chính ở IoU 0.50 và đối chiếu 0.30/0.70 trong iou_sweep.md",
     "IoU 0.50 là ngưỡng matcher của lab; sweep cho thấy edge gãy ở cả 0.70 nên kết luận không phụ thuộc ngưỡng",
     "accepted"),
]
write_csv(sub / "40_decision_log.csv", DECISION_HEADER, DECISIONS)

SAMPLING_HEADER = "camera_id,slice_type,frames,risk,rationale".split(",")
SAMPLING = [
    ("front", "normal", 30, "medium",
     "Camera trước là vùng nhìn chính của ADASIND; mật độ vật trung bình nên dùng làm mốc độ phủ."),
    ("front", "hard", 30, "high",
     "Vật bị vòng kính cắt và xe ba bánh nhỏ ở xa là hai lỗi người gán hay gặp nhất trong findings.csv."),
    ("rear", "normal", 25, "medium",
     "Camera sau ít vật hơn nhưng góc chết sát ego_body; cần frame để soát lại lens_border."),
    ("rear", "hard", 25, "high",
     "Cụm phương tiện bám đuôi và biển số mờ làm nguy cơ bỏ sót vật nhỏ cao."),
    ("left", "normal", 20, "low",
     "Làn trái phần lớn trống; tăng tỷ lệ này sẽ tiêu ngân sách 200 frame mà ít ca khó."),
    ("left", "hard", 20, "high",
     "Vật đi vào từ mép trái rất nhanh và dễ bị cắt nửa box nên cần hard slice riêng."),
    ("right", "normal", 25, "medium",
     "Vùng seam phải với camera sau; dùng để soát vật xuất hiện hai lần."),
    ("right", "hard", 25, "high",
     "Seam phải là nơi dễ sinh DUPLICATE nhất; cần frame để thử policy cross-camera."),
]
write_csv(sub / "45_sampling_plan.csv", SAMPLING_HEADER, SAMPLING)

rows = read_rows(sub / "findings.csv")
errors = validate_rows(rows)
print("findings rows:", len(rows))
print("validation errors:", len(errors))
for error in errors:
    print("  " + error)
print("sampling frames total:", sum(row[2] for row in SAMPLING))
print("decision rows:", len(DECISIONS))




