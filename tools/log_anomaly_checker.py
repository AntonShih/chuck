# 錯誤紀錄
import json

def log_anomalies(data, log_path="anomaly_log.txt"):
    logs = []
    for item in data:
        article = item["article"]
        content = item["content"]
        clauses = item.get("clauses", [])

        if len(content) < 5 and not clauses:
            logs.append(f"[EMPTY] {article} 沒有主文也沒有條款")

        if len(clauses) == 0:
            logs.append(f"[NO_CLAUSE] {article} 沒有條款")
        if len(clauses) > 20:
            logs.append(f"[TOO_MANY_CLAUSES] {article} 條款超過 20 筆")

        clause_numbers = [c["number"] for c in clauses]
        if len(set(clause_numbers)) < len(clause_numbers):
            logs.append(f"[DUPLICATE_CLAUSE] {article} 條號有重複：{clause_numbers}")

        for clause in clauses:
            if clause["text"].count("。") > 2 or len(clause["text"]) > 100:
                logs.append(f"[LONG_CLAUSE] {article} 第 {clause['number']} 款 可能為段落混入")

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(logs))

    print(f"✅ Anomaly log 已儲存至 {log_path}，共發現 {len(logs)} 條可疑紀錄")

# ✅ 直接執行這支檔案也能運作
if __name__ == "__main__":
    input_path = "data/useful_cleaned.json"
    output_path = "log/anomaly_log.txt"

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    log_anomalies(data, output_path)
