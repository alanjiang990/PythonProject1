# 📡 Trajectory Analysis System
### 即時軌跡監控與歷史數據分析平台

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

> **Overview**
> 本專案是一套專為室內定位設計的視覺化系統，包含 **即時監控** 與 **歷史回放** 兩大模組。
> 介面採用現代化深色風格 (Dark Theme)，優化長時間監控的視覺體驗，並整合 Matplotlib 進行高精度繪圖。

---

## 📸 System Preview (系統預覽)

| **Real-time Monitor (即時監控)** | **History Analytics (歷史分析)** |
|:---:|:---:|
| <img src="放入你的截圖1.png" width="400"/> | <img src="放入你的截圖2.png" width="400"/> |
| *即時顯示多目標軌跡與特殊點位* | *時間軸回放與多玩家數據篩選* |

---

## 🛠️ Installation (安裝需求)

確保已安裝 Python 3.8+，並執行以下指令安裝依賴套件：

```bash
pip install PyQt6 pandas matplotlib numpy
(資料庫使用內建 SQLite3，無須額外安裝)🚀 Module 1: Real-time Monitor (即時監控)Script: gui_realtime.py此模組負責接收感測器數據 (Sensor Data)，並即時將座標繪製於畫布上。🎮 Control Panel (左側控制面板)區塊功能說明🗺️ 地圖設定瀏覽底圖：支援載入 .png/.jpg 平面圖，自動疊加於座標系底層 (預設 0-100)。⭐ 特殊點設定載入 CSV：標記場域內的危險區或重要地標。顯示開關：可隨時隱藏或顯示特殊點圖層。⚙️ 顯示參數軌跡保留點數：控制「貪食蛇」長度。• Low (5-10): 畫面簡潔，僅關注當下。• High (50+): 顯示完整移動路徑。👥 玩家列表即時狀態：顯示偵測到的 ID。自訂名稱：點擊名稱欄位可直接修改 (如 Target A)，系統自動記憶。勾選過濾：取消勾選可隱藏特定目標。📈 Module 2: History Analytics (歷史分析)Script: gui_history.py此模組用於回放過去的錄製資料，支援時間軸切片與多目標交叉分析。🔍 Core Features (核心功能)📅 Session Selector (場次選擇)自動列出所有錄製時段 (Time + SessionID)。支援快速切換不同測試場次。🔍 Advanced Filtering (進階篩選)Player Filter: 支援多選，僅查看特定目標的互動。Auto-Save: 玩家的改名紀錄會同步儲存至 json 檔。⏱️ Time Slider (時間軸滑桿)雙向滑桿: 位於底部面板。可拖曳 Start 與 End 端點，精準限縮觀察的時間區間 (例如：只看發生異常的那 30 秒)。📂 File Structure (檔案結構)PlaintextProject Root/
├── 📂 assets/              # 存放底圖資源
├── 📜 gui_realtime.py      # [APP] 即時監控主程式
├── 📜 gui_history.py       # [APP] 歷史分析主程式
├── 📜 backend_logic.py     # [Logic] 定位演算與 DB 寫入
├── 🗃️ history_records.db   # [Data] 軌跡數據庫 (SQLite)
├── ⚙️ player_settings.json # [Config] 玩家名稱記憶檔
└── 📄 README.md            # 說明文件
📝 Appendix: CSV Format若需匯入 特殊點 (Special Points)，請使用以下 CSV 格式：程式碼片段name, x, y
Base Station A, 10.5, 20.0
Obstacle 1, 50.0, 50.0
Exit, 95.0, 95.0
Note for Developers系統預設背景色為 #1e1e1e (Dark Grey)。資料庫建議開啟 WAL 模式以獲得最佳寫入效能。
