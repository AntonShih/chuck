# 玩勞動基準法清整的程式
import re
import json

def clean_text(text: str) -> str:
    # 移除無語意特殊符號
    text = re.sub(r"[★☆●◆※→←◎▲○●•・~■▶▼＊＿╱╲｜│┃─═＝—_…]", "", text)
    # 移除不可見字元與多餘空白
    text = re.sub(r"[ \t\u200b]+", " ", text)
    # 合併連續換行
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()

def extract_qa_pairs(text: str) -> list:
    # 假設 Q: 開頭是問題，A: 開頭是回答
    qa_pattern = re.compile(r"(Q[:：](.+?))\n*A[:：](.+?)(?=(?:\nQ[:：])|\Z)", re.DOTALL | re.IGNORECASE)
    matches = qa_pattern.findall(text)

    qa_pairs = []
    for full_q, q, a in matches:
        q_clean = clean_text(q.strip().replace("\n", " "))
        a_clean = clean_text(a.strip().replace("\n", " "))
        if q_clean and a_clean:
            qa_pairs.append({
                "question": q_clean,
                "answer": a_clean
            })

    return qa_pairs

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_json(data: list, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    input_path = "data/Labor_Standards_Act7.txt"      # ✅ 輸入原始 FAQ 檔
    output_path = "data/Labor_Standards_Act7_cleaned.json"       # ✅ 輸出清洗後 JSON

    raw_text = load_text(input_path)
    qa_list = extract_qa_pairs(raw_text)
    save_json(qa_list, output_path)

    print(f"✅ 完成：擷取 {len(qa_list)} 筆 QA 並儲存至 {output_path}")
