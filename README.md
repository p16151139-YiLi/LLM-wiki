# SiC LLM Wiki × 教學 HTML 簡報

這是一份可離線開啟、可直接部署到 GitHub Pages 的靜態 HTML 教學專案。

## 怎麼開啟
- `index.html`：專案入口，連結 Wiki 與簡報。
- `wiki/index.html`：六章學習內容，可搜尋章節，每篇對應證據卡與來源。
- `slides/index.html`：13 頁 HTML 簡報；可按左右方向鍵、上一頁／下一頁、觸控滑動；「⎙」為列印成 PDF。

## 六篇已 ingest 的來源
`source_manifest.json`、`raw/S01.md`～`raw/S06.md`。**Ingest 是從公開全文或公開摘要進行的原創中文事實摘記，不代表把所有論文全文存進專案。** 每筆明確標明哪篇全文可讀、哪篇只取得摘要。

## Wiki 與投影片對照
- Wiki 6 個章節：`wiki/*.md`，公開版 `wiki/index.html`
- 證據卡：`cards/E01.md`～`cards/E12.md`
- 逐頁稿與引用：`slides/drafts/`、`slides/slide_manifest.json`
- 最後的 HTML：`slides/index.html`
- Workflow 與反思：`workflow_graph.mmd`、`.agents/workflows/topic-slides.md`、`report.md`

## 驗證
```bash
python qa/check.py
```
另外可執行 `node qa/test_interactions.js`（無需另外安裝套件），檢查操作邏輯。`qa/` 中有靜態檢查 19/19、Node 模擬 DOM 行為 12/12、WeasyPrint 13 頁預覽；**真實 Chromium 自動化受此環境管理政策攔截，未通過**。請於自己電腦開啟 `index.html` 按 `qa/manual_browser_checklist.md` 驗收。

## 發佈 GitHub Pages（需自行操作）
1. 在 GitHub 建立新的公開 Repository（例如 `sic-llm-wiki`）。
2. 解壓縮後，**把本專案資料夾裡面的檔案**上傳到 Repository 根目錄，必須有最上層 `index.html`。
3. 到 Settings → Pages → Build and deployment → Deploy from a branch；選 `main` 與 `/ (root)`，儲存。
4. 等 GitHub Pages 顯示部署完成後，複製實際 URL：首頁 `https://帳號.github.io/儲存庫名稱/`；Wiki `.../wiki/`；簡報 `.../slides/`。
5. 把 **實際能打開的網址** 貼到 `submission.txt` 的空白處。這些 URL 是格式示範，不是假定已發布的網址。

## 注意事項
- 某些來源可能受付費或地區限制；本站本地內容不需要存取外部網路，點原始連結才需要。
- 本專案並不是連接即時 LLM API 的問答服務，而是由 LLM 輔助整理出的**靜態 LLM Wiki**，透過來源 ID 與卡片可追溯。
- 如需同學自行再次 ingestion / 生成，請依 `AGENTS.md` 和 workflow 規格操作；HTML 不會自動產生新內容。
- 繳交時需據實填學校、學號、系級、姓名，並自行部署網址；未經實作的人工審查／訪談畫面不可宣稱完成。
