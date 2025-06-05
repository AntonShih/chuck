# 肉眼發現有問題而合併回去的程式
import json

def clean_json_structure(data):
    cleaned = []
    for i, item in enumerate(data):
        # 預處理：去除全形/半形空格
        item["content"] = item["content"].replace(" ", "").replace("　", "").strip()

        for clause in item.get("clauses", []):
            clause["text"] = clause["text"].replace(" ", "").replace("　", "").strip(" 。.1234567890 ")

        # 🚫 第三十二條其實是第一條的一部分，要合併回去
        if item["article"] == "第三十二條":
            if cleaned:
                cleaned[-1]["content"] += item["article"] + item["content"]
            continue


        # 🔧 修正第三條第六款被夾帶過多句子
        if item["article"] == "第三條":
            for clause in item["clauses"]:
                if clause["number"] == "六" and "開除學籍" in clause["text"]:
                    parts = clause["text"].split("。", 1)
                    clause["text"] = parts[0].strip()
                    if len(parts) > 1:
                        item["content"] += parts[1].replace(" ", "").replace("　", "").strip()

        # 🧯 空 content 處理
        if item["content"].strip() == "":
            item["content"] = "本條僅包含條款，無主文敘述。"

        cleaned.append(item)
    return cleaned


# ✅ 主程式入口
if __name__ == "__main__":
    input_path = "data/useful.json"
    output_path = "data/useful_cleaned.json"

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_data = clean_json_structure(data)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 清理完成，所有空格已移除，輸出檔案：{output_path}")

