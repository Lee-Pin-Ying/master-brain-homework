# 碩班外接大腦

由 AI 協助維護的長期學習知識庫。第一個主題是「GPS 訊號不佳時的跑步配速校正」。本次成果是來源、Wiki 與靜態 HTML 展示，尚未實作配速模型。

## 開啟展示
直接雙擊根目錄 index.html；不需要 Node.js、套件安裝或 API 金鑰。
三個內頁為研究構想、文獻方法比較、資料與驗證規劃。可捲動閱讀、用頁內按鈕／方向鍵切段，或由瀏覽器列印。

## 檔案結構
- AGENTS.md：跨主題通用 AI 工作規則。
- raw/：Notion 研究構想、兩份論文 PDF、四筆論文清單與取得狀態。
- wiki/index.md：全庫筆記目錄。
- wiki/gps/：研究概述、來源筆記、概念、綜合比較與待確認事項。
- wiki/log.md：操作紀錄。
- pages/gps/：三個 HTML 展示內頁。
- assets/：本地共用 CSS 與段落導覽 JavaScript。
- index.html：展示首頁。

## 生成與更新 SOP
1. 選擇可信來源，放入 raw；保留來源與版本。
2. 請 AI 先讀 AGENTS.md，再執行 Ingest：閱讀、更新來源筆記與概念、加入交叉連結。
3. 更新 wiki/index.md 與 wiki/log.md；未知事項寫進 pending。
4. 需要報告時，根據 Wiki 生成／更新 HTML 與首頁。
5. 檢查來源、數字、連結與手機排版。

示範指令：「請先讀 AGENTS.md，收錄 raw 裡的新資料，更新 GPS 主題相關筆記與索引，回報尚未確認的事項。這次不用生成簡報。」

## 本次來源與限制
- S01：使用者 Notion 研究構想，屬需求與假說。
- S02：Zrenner et al. (2018)，DOI https://doi.org/10.3390/s18124194 。閱讀研究章節；鞋上 IMU 研究，不能直接推廣為手腕效果。PDF p.22 標示 CC BY 4.0；作者署名詳來源筆記。
- S03：Zhong et al.，https://arxiv.org/abs/2212.14264v2 ，本地為 2023 arXiv v2。研究行人手機定位，即時滑動視窗列為未來工作；PDF 再散布授權未確認。
- S04、S05 僅本地書目，尚無 PDF 全文。
- 尚無個人活動檔分析、模型訓練、獨立速度驗證與手錶部署。
- HTML 中軌跡圖為原創概念示意，非實測數據。
- 內頁 Markdown 連結在瀏覽器可能顯示純文字或下載；HTML 導覽不依賴 Markdown 渲染。

## GitHub 繳交
將可公開的完整專案提交，包括 AGENTS.md、raw 來源描述與允許再散布的材料、wiki、assets、pages、index.html 與本說明。請勿只交 HTML。
S03 本地 PDF 暫以 .gitignore 排除；公開版本保留文獻入口與下載指令，待授權確認再決定是否納入。PDF 不在 GitHub 時，原始檔連結需先依下方指令補回本機；HTML 的外部原文連結仍可使用。
GitHub Pages 如啟用，選擇儲存庫根目錄作為網站來源。尚未建立或上傳 GitHub 儲存庫。

補回 S03 PDF（PowerShell，在專案根目錄執行）：
```powershell
Invoke-WebRequest -Uri 'https://arxiv.org/pdf/2212.14264v2' -OutFile 'raw/zhong-2023-gnss-pdr-fgo.pdf'
```
尚未確認的再散布授權不能由「可下載」推定；本機閱讀可保留原檔。
