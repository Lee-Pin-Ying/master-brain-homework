# GPS 訊號不佳時的跑步配速校正
類型：使用者研究構想與第一份展示需求範圍；尚未實作或驗證模型。

## 問題與方向
高樓遮蔽可能造成 GPS 漂移與手錶配速跳動。構想是評估 GPS 可信度，結合步伐與動作資訊估計速度，輸出配速與可信度。[S01](../../raw/gps/research-proposal.md)
必須避免用同段失準 GPS 推得的步長，重新證明 GPS 已被校正。

## 第一份展示需求
讀者預設為具基本 AI 知識但不熟 GNSS／IMU 的老師同學。
此主題先建立有來源、相互連結的 Wiki，並已製作淺色簡潔靜態 HTML：研究構想、方法比較、資料與驗證規劃三個內頁，由根目錄 index.html 連入。
這些是本次展示需求，不限制其他主題。

## 來源狀態
- S01：Notion 研究構想，已讀；屬需求與假說。
- S02：[Zrenner 2018 閱讀筆記](sources/zrenner-2018.md)，已閱讀 PDF 主要研究內容 pp.1–20；文末參考書目非逐篇已讀。
- S03：[Zhong arXiv v2 閱讀筆記](sources/zhong-2023.md)，已閱讀研究內容 pp.1–9；參考文獻非逐篇已讀。
- S04、S05：[待補全文](pending.md)，僅本地書目與既有 Notion 說明。

## 先看這些
- [感測器位置與方法遷移](concepts/sensor-placement.md)
- [即時估計、平滑與驗證](concepts/realtime-validation.md)
- [方法比較與驗證規劃](syntheses/method-comparison.md)
- [待確認問題](pending.md)

## 原始來源
[S01 研究構想](../../raw/gps/research-proposal.md)；[Notion 原頁](https://app.notion.com/p/3ed463f571d681b7b045f16826e826d7)。
本輪未使用任何真實跑步活動檔進行模型訓練或效能驗證。

