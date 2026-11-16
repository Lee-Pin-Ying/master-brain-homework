# S02｜鞋上 IMU 跑步速度與步長演算法比較
狀態：已閱讀本地 PDF 的研究內容 pp.1–20；圖表數值以所列頁碼核對。
來源：[PDF](../../../raw/zrenner-2018-running-imu-algorithms.pdf)；[DOI](https://doi.org/10.3390/s18124194)。
作者：Markus Zrenner、Stefan Gradl、Ulf Jensen、Martin Ullrich、Bjoern M. Eskofier；2018。

## 研究設計
- 感測器放在跑鞋中底，不是手腕。加速度計與陀螺儀採樣 200 Hz。（§2.1，pp.3–5）
- 實驗室：27 位跑者、2377 個跨步，速度範圍 2–6 m/s，以 3D 動作捕捉為參考。（§2.1.1，pp.3–4）
- 戶外：另外 12 人完成 400 m 跑道八圈、共 3.2 km，以已知總距離驗證；另比較手機 GPS。（§2.1.2，p.5）
- 輸出主要是每個跨步的平均速度、跨步長度，以及累積距離，並非驗證高樓環境的手錶即時配速。

## 四種方法
| 方法 | 主要資訊 | 建模／訓練需求 |
|---|---|---|
| Stride time | 跨步時間、身高、性別與文獻關係 | 使用查表規則，個體差異限制明顯 |
| Acceleration | 三軸足部加速度特徵 | 二次迴歸模型，需參考速度訓練 |
| Trajectory | 加速度與角速度，重建足部軌跡 | 去重力、積分、跨步去漂移；此法無模型訓練階段 |
| Deep Learning | 分段後的六軸 IMU | CNN 回歸跨步長度，再除以跨步時間 |

方法定位：§2.2，pp.5–12；Acceleration 與 Deep Learning 以留一受試者交叉驗證評估（§2.3，p.12）。

## 具體結果與適用條件
實驗室 Table 4（p.13）的速度 MAE：Stride time 0.622、Acceleration 0.272、Trajectory 0.133、Deep Learning 0.216 m/s。
同表 Trajectory 速度 ME ± Std 為 0.028 ± 0.252 m/s。摘要 p.1 的 0.032 ± 0.274 m/s 與表格不同，後續展示須明確引用 Table 4，不能混寫成同一組結果。
戶外 3.2 km 總距離 MAE：Trajectory 94.0 m，GPS 82.1 m（§3.2，p.15）。這不是即時速度誤差，也未顯示此試驗中 IMU 優於 GPS。

## 限制與對本題的啟發
- 足部軌跡法的零速度假設在較高速跑步時受限制（§4.2，p.17）；不能直接套在持續擺動的手腕。
- 論文指出 Acceleration 可降至 60 Hz 且在其實驗室資料中未影響精度（p.17）；不能視為所有手錶的保證。
- 本題可借鏡基準比較與驗證方法；移植手腕、都市遮蔽與即時延遲都仍待測試。
- PDF p.22 標示 CC BY 4.0，公開時仍須保留作者、來源與授權資訊。

## 相關筆記
[感測器位置](../concepts/sensor-placement.md)｜[驗證指標](../concepts/realtime-validation.md)｜[方法比較](../syntheses/method-comparison.md)

