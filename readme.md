# 📘 條文清理與 QA 擷取工具包

本專案提供一套針對中文條文（如：國立臺灣大學學生個人獎懲辦法、勞動基準法）所設計的清理、結構化、問答擷取與異常檢查流程。可應用於 AI 語意檢索（RAG）、FAQ 建構、法規結構化等任務。

---

## 📂 專案目錄架構

```bash
.
├── tools/
│   ├── pdf_loader.py              # PDF → 純文字
│   ├── text_cleaner.py            # 條文語意清洗（保留段落 / 扁平版本）
│   ├── useful_ntu.py              # 條文轉條+款 JSON 結構
│   ├── useful_clean.py            # 條文結構修補（合併錯誤條、修正文句）
│   ├── extract_clean_qa_pairs.py  # 擷取勞基法 FAQ（Q: A: 格式）
│   ├── split_ntu_rule.py          # 多種 chunk 切段策略（固定、語意）
│   ├── log_anomaly_checker.py     # 條文異常檢查
├── data/                          # 存放處理中間與最終資料
└── log/                           # 異常記錄輸出
