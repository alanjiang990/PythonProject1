# 📡 Trajectory Tracking & Analytics System
### 軌跡追蹤與分析系統

> **System Overview**
> 本專案包含兩大核心模組：**即時監控 (Real-time Monitor)** 與 **歷史分析 (History Analytics)**。
> 介面採用現代化深色風格 (Dark Theme)，專為長時間監控與數據分析設計。

---

## 🛠️ 環境需求 (Prerequisites)

請確保已安裝 Python 3.8+ 以及以下必要套件：

```bash
pip install PyQt6 pandas matplotlib numpy
(註：sqlite3 為 Python 內建標準庫，無須額外安裝)

🚀 1. 即時監控系統 (Real-time Monitor)
程式入口: gui_realtime.py (假設檔案名稱)

此模組負責接收感測器數據，並即時繪製玩家/物件的移動軌跡。

🎮 介面功能說明 (Interface Guide)
左側：控制面板 (Control Panel)
所有操作均集中於左側深色面板，由上而下功能如下：

🗺️ 地圖設定 (Map Settings)

瀏覽 (Browse): 點擊載入場域平面圖 (.png, .jpg)。

系統會自動將圖片疊加於座標系底層 (預設範圍 0-100)。

⭐ 特殊點設定 (Special Points)

瀏覽 (Browse): 載入標註重要位置的 CSV 檔案 (格式需包含 x, y 欄位)。

顯示核取方塊: 可隨時開啟或關閉特殊點的顯示。

⚙️ 顯示參數 (Display Params)

軌跡保留點數: 設定畫面上的「貪食蛇」長度。

數值越小：畫面越簡潔，僅顯示最新位置。

數值越大：顯示較長的歷史路徑。

👥 玩家列表 (Player List)

ID / 名稱: 表格顯示偵測到的玩家 ID。

自訂名稱: 點擊「名稱」欄位可直接修改 (例如將 Player 1 改為 Target Alpha)，系統會自動記憶。

勾選過濾: 取消勾選可暫時隱藏特定玩家的軌跡。

▶️ 開始監控 (Start Button)

藍色按鈕。點擊後系統開始寫入 Session 並即時更新畫面。

右側：視覺化區域 (Visualizer)
深色畫布: 採用 #1e1e1e 背景，減少螢幕眩光。

動態繪圖: 自動更新最新位置、繪製移動路徑，並以不同顏色區分玩家。

📈 2. 歷史軌跡分析系統 (History Analytics)
程式入口: gui_history.py (假設檔案名稱)

此模組用於回放與深度分析過去的錄製資料。

🔍 介面功能說明
Session Selector (場次選擇)

從下拉選單選擇歷史錄製時段 (包含日期與 Session ID)。

Player Filter (玩家篩選)

支援多選。選擇該場次中想關注的特定目標。

同樣支援讀取/寫入自訂名稱記憶。

Data Loading (載入資料)

點擊 LOAD DATA 後，系統會從資料庫撈取符合條件的點位。

Time Slider (時間軸滑桿)

位於底部。拖動雙向滑桿可限縮時間範圍 (例如：只看前 10 分鐘的軌跡)。

上方會即時顯示選取區間的 Start Time 與 End Time。

📂 檔案結構 (File Structure)
Plaintext

Project/
├── history_records.db     # [Core] 儲存所有軌跡與場次數據的資料庫
├── player_settings.json   # [Config] 儲存玩家自訂名稱與顯示設定
├── gui_realtime.py        # [App] 即時監控主程式
├── gui_history.py         # [App] 歷史分析主程式
├── backend_logic.py       # [Logic] 後端運算與資料庫寫入邏輯
├── init_point.csv         # [Config] 基站座標設定
└── assets/                # 存放底圖或圖標
📝 CSV 格式規範
若需匯入 特殊點 (Special Points)，CSV 檔案內容請參照以下格式：

程式碼片段

name,x,y
Point A,10.5,20.0
Point B,50.0,50.0
Danger Zone,85.2,90.1
Note: 系統預設使用 SQLite WAL 模式以支援高頻率讀寫。若直接移動 .db 檔案，請確保連同 .db-shm 與 .db-wal 一併移動，或在程式完全關閉後再進行操作。
