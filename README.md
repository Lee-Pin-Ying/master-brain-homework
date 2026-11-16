# 碩士班知識庫

依主題整理論文、課程、研究與作業的個人知識庫。AI 協助整理與維護，使用者負責挑來源、閱讀、提問與決定方向。目前第一個主題是 GPS 跑步配速研究。

## 開啟
- 直接雙擊根目錄 index.html，不需啟動 Node.js。
- 首頁選主題 → 原始資料、知識筆記、簡報與展示。
- 原始資料與簡報區也有全庫入口，依主題分類。
- Wiki 同時保留 Markdown 與網頁版；Obsidian 開啟整個資料夾即可讀原始筆記。

## 分工
AGENTS.md 是全庫通用規則；具體研究內容、讀者、單次作業要求放在 wiki/<slug>/overview.md。
raw/<slug>/ 保留來源；wiki/<slug>/ 保存理解與連結；pages/<slug>/ 放按需產生的展示。
topics.json 登錄實際已有的主題、來源與展示，scripts/build.py 產生首頁與索引。

## 更新流程
1. 將新來源放進對應 raw/<slug>/，記錄來源網址與取得狀態。
2. 請 AI 先讀 AGENTS.md，再整理來源筆記、概念與比較，更新索引與紀錄。
3. 在 topics.json 更新來源與展示清單。
4. 執行 python scripts/build.py，生成主題入口、來源清單、Wiki 網頁與簡報目錄。
5. 檢查本地連結與手機排版；授權發布後提交 GitHub。

Python 生成器僅用標準函式庫，不需要安裝套件；如系統沒有 python 指令，指定可用的 Python 執行檔。
生成器不更動原始來源、Markdown 筆記與已存在的展示內頁；這些內容由 AI 依指示編輯。
不要直接修改生成的首頁／索引／Wiki HTML，應修改 topics.json、Markdown 或 scripts/build.py 後重建。

## 新增主題
依 AGENTS.md 的「新增一個主題」流程，建立 raw/<slug>/ 與 wiki/<slug>/overview.md，再於 topics.json 增加一筆主題。
例如之後加入 machine-learning，重建後首頁會出現它；不需要複製整個知識庫，也不強迫先做簡報。

## 展示與限制
GPS 的三個展示頁屬第一份研究介紹，並非整個知識庫的永久主題。既有 pages/gps/problem.html、methods.html、validation.html 網址保持不變。
目前尚無個人跑步資料實驗、配速模型訓練與手錶部署。
放入 raw 不會自動觸發 AI；需啟動代理並交代處理，也不會自動上傳 GitHub。

## 來源與公開範圍
S01 是使用者構想。S02 Zrenner et al. (2018)，DOI https://doi.org/10.3390/s18124194 ，PDF p.22 標示 CC BY 4.0；作者與適用限制見 Wiki。
S03 Zhong et al. arXiv v2：https://arxiv.org/abs/2212.14264v2 ，本地 PDF 再散布授權未確認，以 .gitignore 排除，網站直接連到原文。S04、S05 全文仍待取得。
raw/gps/README.md 保留首次取得紀錄，因此其中檔名依舊存在，但舊記錄中的資料夾配置以本說明為準。
公開的儲存庫只包含已授權的主題；未來新增私人資料不代表自動授權公開。

## 部署
沿用 GitHub Pages：main 分支、/(root)。.nojekyll 讓 HTML 和來源檔以靜態檔案提供，不轉換 Markdown。更新後仍需等待 GitHub 部署完成。

- 專案：https://github.com/Lee-Pin-Ying/master-brain-homework
- 網站：https://lee-pin-ying.github.io/master-brain-homework/
