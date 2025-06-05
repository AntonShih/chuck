# 可視化跟適合拿來扁平的檔案
import re

def strip_page_artifacts(text: str) -> str:
    """移除 PDF 殘留的頁碼與頁首雜訊，例如「第12頁」、獨立數字行等。"""
    text = re.sub(r"第\s*\d+\s*頁", "", text)
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text

def merge_hard_wrapped_lines(text: str) -> str:
    """合併非語意段落的硬換行（如一行一句），避免誤傷條文開頭。"""
    # 條文開頭保護
    text = re.sub(r"(?<!\n)(第[一二三四五六七八九十百\d]+條)", r"\n\1", text)

    # 合併句中換行（非標點結尾 + 非條文開頭）
    pattern = r"(?<![。；：？！)])\n(?!\n|第[一二三四五六七八九十百\d]+條)"
    text = re.sub(pattern, " ", text)
    return text

def restore_readability(text: str) -> str:
    """格式化條文為語意清晰結構：條文 → 子項 → 句段。"""
    text = re.sub(r"(?<![^\n])(第[一二三四五六七八九十百\d]+條)", r"\n\n\1\n", text)
    text = re.sub(r"(?<!第)(?<!條)([一二三四五六七八九十百]+、)", r"\n\1", text)
    text = re.sub(r"(\d{2,3}\.\d+\.\d+[^ \n]*)", r"\n\1", text)
    text = re.sub(r"(?<=[。！？；])(?=[^\n])", "\n", text)
    text = re.sub(r"\n\s*(得|應|如|但|則|亦|若|經|前項|後項|此外|或|並|故)", r"\n\n\1", text)
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def clean_for_vector_db(text: str) -> str:
    """用於向量庫前的最終清洗：去除所有換行與多空格。"""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_ntu_rule(raw_text: str, for_vector_db: bool = False) -> str:
    """條文清理管線，可選是否用於向量庫。"""
    text = strip_page_artifacts(raw_text)
    text = merge_hard_wrapped_lines(text)
    text = restore_readability(text)
    return clean_for_vector_db(text) if for_vector_db else text

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_text(text: str, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    raw = load_text("data/NTU_rule.txt")

    # ✅ 用於閱讀與展示
    cleaned = clean_ntu_rule(raw)
    save_text(cleaned, "data/final_NTU_rule.txt")

    # ✅ 用於切 chunk、向量上傳
    cleaned_flat = clean_ntu_rule(raw, for_vector_db=True)
    save_text(cleaned_flat, "data/final_NTU_rule_flat.txt")

    print("✅ 條文清理完成：")
    print("- final_NTU_rule.txt（保留段落結構）")
    print("- final_NTU_rule_flat.txt（用於向量庫）")
