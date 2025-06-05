import re

def strip_page_artifacts(text: str) -> str:
    """
    移除 PDF 殘留的頁碼與頁首雜訊，例如「第12頁」、獨立數字行等。
    """
    text = re.sub(r"第\s*\d+\s*頁", "", text)
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text


def merge_hard_wrapped_lines(text: str) -> str:
    """
    合併中文句子內被機器硬切的換行（非標點結尾），避免把「第X條」合併。
    """
    # 保護條文標題不被合併
    text = re.sub(r"(?<!\n)(第[一二三四五六七八九十百\d]+條)", r"\n\1", text)

    # 合併非標點結尾的換行，避免合併條文開頭
    pattern = r"(?<![。；：？！)])\n(?!\n|第[一二三四五六七八九十百\d]+條)"
    return re.sub(pattern, " ", text)


def restore_readability(text: str) -> str:
    """
    條文格式化 v2：結構清晰、語意完整、便於閱讀與切段。
    """
    # 條文標題換段：只針對行首的「第X條」
    text = re.sub(r"(?<![^\n])(第[一二三四五六七八九十百\d]+條)", r"\n\n\1\n", text)

    # 子項目如「一、二、三」換行（避免誤切「第十條」）
    text = re.sub(r"(?<!第)(?<!條)([一二三四五六七八九十百]+、)", r"\n\1", text)

    # 年月日沿革切行
    text = re.sub(r"(\d{2,3}\.\d+\.\d+[^ \n]*)", r"\n\1", text)

    # 中文標點後（句點、問號、感嘆號、分號）自動換行，排除句中逗號（、）
    text = re.sub(r"(?<=[。！？；])(?=[^\n])", "\n", text)

    # 條內補述語意切段（如 得、但、應、如、前項…）
    text = re.sub(r"\n\s*(得|應|如|但|則|亦|若|經|前項|後項|此外|或|並|故)", r"\n\n\1", text)

    # 清除空白與壓縮多餘換行
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_ntu_rule(raw_text: str) -> str:
    """
    清理 + 格式化條文文字，提升閱讀性與結構層次。
    """
    text = strip_page_artifacts(raw_text)
    text = merge_hard_wrapped_lines(text)
    text = restore_readability(text)
    return text


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_text(text: str, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    raw = load_text("data/NTU_rule.txt")
    cleaned = clean_ntu_rule(raw)
    save_text(cleaned, "data/final_NTU_rule.txt")
    print("✅ 條文清理與格式化完成，輸出至 final_NTU_rule.txt")
