# 各種切法
import json
from typing import List, Dict

# ✅ 固定字數切法（baseline）
def split_by_fixed_length(text: str, max_chars: int = 300) -> List[Dict]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end].strip()
        chunks.append({"chunk": chunk})
        start = end
    return chunks


def split_by_langchain_short(text: str, chunk_size: int = 100, chunk_overlap: int = 20) -> List[Dict]:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        raise ImportError("請先安裝 langchain：pip install langchain")

    splitter = RecursiveCharacterTextSplitter(
        separators=[""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    documents = splitter.create_documents([text])
    return [{"chunk": doc.page_content} for doc in documents]

def split_by_langchain_mid(text: str, chunk_size: int = 200, chunk_overlap: int = 40) -> List[Dict]:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        raise ImportError("請先安裝 langchain：pip install langchain")

    splitter = RecursiveCharacterTextSplitter(
        separators=[""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    documents = splitter.create_documents([text])
    return [{"chunk": doc.page_content} for doc in documents]


# ✅ 語意切（LangChain）
def split_by_langchain_long(text: str, chunk_size: int = 300, chunk_overlap: int = 60) -> List[Dict]:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        raise ImportError("請先安裝 langchain：pip install langchain")

    splitter = RecursiveCharacterTextSplitter(
        separators=[""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    documents = splitter.create_documents([text])
    return [{"chunk": doc.page_content} for doc in documents]


# ✅ 輸入與輸出
def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_json(data: List[Dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    raw_text = load_text("data/final_NTU_rule_flat.txt")

    # 🟦 執行4種切法
    fixed_chunks = split_by_fixed_length(raw_text)
    langchain_chunks_short = split_by_langchain_short(raw_text)
    langchain_chunks_mid = split_by_langchain_mid(raw_text)
    langchain_chunks_long = split_by_langchain_long(raw_text)

    # 🟨 儲存成 JSON
    save_json(fixed_chunks, "data/ntu_chunks_fixed.json")
    save_json(langchain_chunks_short, "data/ntu_chunks_langchain_short.json")
    save_json(langchain_chunks_mid, "data/ntu_chunks_langchain_mid.json")
    save_json(langchain_chunks_long, "data/ntu_chunks_langchain_long.json")

    print("4種切法已完成輸出！")


