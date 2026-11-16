# 原始資料目錄

依主題保存來源，來源內容與 Wiki 整理分開。

- [GPS 原始資料網頁](gps/index.html)：論文名稱、閱讀狀態與原文連結。
- [GPS 原始來源紀錄](gps/README.md)：首次收集時保存的取得紀錄。

新增主題時建立 raw/<slug>/，在 topics.json 登錄來源，再執行 python scripts/build.py。
原始文獻不改寫；自動生成的 index.html 可重建。
