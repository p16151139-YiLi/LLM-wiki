# 真實瀏覽器測試嘗試（尚未通過；誠實記錄）

檢查日期：2026-11-12

- 測試工具：Python Playwright + 系統 Chromium 144。
- 首次以 `file:///.../slides/index.html` 進入，收到 `net::ERR_BLOCKED_BY_ADMINISTRATOR`。
- 第二次以本機 Python HTTP Server 的 `http://127.0.0.1:8765/slides/index.html` 進入，仍收到相同管理政策攔截。
- 結論：這是測試容器的環境限制，**不代表 HTML 在一般瀏覽器已經驗證成功，也不能由此判斷 HTML 必定錯誤**。
- 替代檢查：實際執行 `node qa/test_interactions.js`（模擬 DOM 行為）得 12/12；`python qa/check.py` 19/19；WeasyPrint 產生 13 頁排版預覽。
- 待補：在使用者本人的 Chrome/Edge 真實開啟 `index.html`，逐頁翻完投影片、測試 Wiki 搜尋並確認所有畫面顯示。
