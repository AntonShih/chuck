import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """從 PDF 擷取所有文字內容"""
    doc = fitz.open(pdf_path)
    all_text = []
    for page in doc:
        text = page.get_text()
        all_text.append(text)
    return "\n".join(all_text)

def save_text_to_file(text: str, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    raw_text = extract_text_from_pdf("data/NTU_rule.pdf")
    save_text_to_file(raw_text, "data/NTU_rule.txt")
    print("✅ PDF 已轉為 NTU_rule.txt")

