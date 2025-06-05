# 經思考過後有用的json格式
import re
import json

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_text(text: str, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def extract_articles_with_clauses(text):
    # 切出每一條：第X條 + 內容（非貪婪到下一條或文件結尾）
    article_pattern = r"(第[一二三四五六七八九十百零○\d]+條)(.*?)(?=第[一二三四五六七八九十百零○\d]+條|$)"
    matches = re.findall(article_pattern, text, re.DOTALL)

    result = []
    for article_number, body in matches:
        body = body.strip().replace('\n', '')  # 去除換行和左右空格

        # 找出所有條款（例：一、xxx。二、xxx。）
        clause_pattern = r"([一二三四五六七八九十百]+)、(.*?)(?=([一二三四五六七八九十百]+)、|$)"
        clause_matches = re.findall(clause_pattern, body)

        # 如果有條款，就分開主文與條款
        if clause_matches:
            first_clause_pos = re.search(r"[一二三四五六七八九十百]+、", body).start()
            main_text = body[:first_clause_pos].strip("：:：.。")
            clauses = [{"number": m[0], "text": m[1].strip("。；; ")} for m in clause_matches]
        else:
            main_text = body
            clauses = []

        result.append({
            "article": article_number,
            "content": main_text,
            "clauses": clauses
        })

    return result

if __name__ == "__main__":
    raw_text = load_text("data/NTU_rule.txt")
    parsed = extract_articles_with_clauses(raw_text)
    save_text(json.dumps(parsed, ensure_ascii=False, indent=2), "data/useful.json")

    print(json.dumps(parsed[:10], ensure_ascii=False, indent=2))
