import csv
import sqlite3
import math
import datetime
import os


def convert_csv_to_db(csv_path, db_path='positioning.db'):
    """
    輸入:
        csv_path: CSV 檔案的完整路徑 (例如 'data/sensor_log.csv')
        db_path:  要儲存的資料庫路徑 (預設為 'positioning.db')
    輸出:
        資料庫的絕對路徑 (Absolute Path)
    """

    # 1. 檢查輸入檔案是否存在
    if not os.path.exists(csv_path):
        print(f"錯誤: 找不到檔案 {csv_path}")
        return None

    # 2. 連接資料庫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("正在清空舊資料庫...")
    cursor.execute("DROP TABLE IF EXISTS points")
    cursor.execute("DROP TABLE IF EXISTS sessions")
    # (保險起見) 確保資料表存在，如果還沒初始化過也不會報錯
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessions
                      (
                          id
                          INTEGER
                          PRIMARY
                          KEY
                          AUTOINCREMENT,
                          name
                          TEXT,
                          start_time
                          TIMESTAMP
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS points
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        session_id
        INTEGER,
        x
        REAL,
        y
        REAL,
        created_at
        TIMESTAMP,
        FOREIGN
        KEY
                      (
        session_id
                      ) REFERENCES sessions
                      (
                          id
                      ))''')

    # 3. 建立新的 Session
    # 使用 CSV 檔名當作這次測試的名稱，方便辨識
    file_name = os.path.basename(csv_path)
    session_name = f"匯入_{file_name}_{datetime.datetime.now().strftime('%H%M%S')}"

    cursor.execute("INSERT INTO sessions (name) VALUES (?)", (session_name,))
    conn.commit()
    current_session_id = cursor.lastrowid

    print(f"正在處理: {csv_path} -> 寫入 Session ID: {current_session_id}")

    # 4. 已知條件 (你的基地台設定)
    d = 100.0  # Anchor B 的 x 座標

    # 5. 讀取並計算
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # 跳過標題列

            count = 0
            for row in reader:
                if not row: continue  # 跳過空行

                # 讀取距離 (假設 CSV 格式: Time, Dist_A, Dist_B, Dist_C)
                try:
                    r_a = float(row[1])
                    r_b = float(row[2])
                    # r_c = float(row[3]) # 目前沒用到
                except (IndexError, ValueError):
                    continue  # 如果這一行數據壞掉，就跳過

                # --- 核心算法 ---
                # x = (r_a^2 - r_b^2 + d^2) / 2d
                x = (r_a ** 2 - r_b ** 2 + d ** 2) / (2 * d)

                # y = sqrt(r_a^2 - x^2)
                temp_y = r_a ** 2 - x ** 2
                if temp_y < 0:
                    y = 0
                else:
                    y = math.sqrt(temp_y)

                # 寫入
                cursor.execute(
                    "INSERT INTO points (session_id, x, y) VALUES (?, ?, ?)",
                    (current_session_id, x, y)
                )
                count += 1

        conn.commit()
        print(f"成功轉換 {count} 筆數據！")

    except Exception as e:
        print(f"處理過程發生錯誤: {e}")
        conn.close()
        return None

    conn.close()

    # 6. 回傳資料庫的「絕對路徑」
    full_db_path = os.path.abspath(db_path)
    return full_db_path


# --- 測試區 (當你直接執行這個檔案時會跑這裡) ---
if __name__ == "__main__":
    # 你可以把這裡換成你實際的 csv 檔名
    input_csv = 'sensor_data.csv'

    # 呼叫函式
    result_db_path = convert_csv_to_db(input_csv)

    if result_db_path:
        print(f"\n任務完成！資料庫位置在:\n{result_db_path}")
    else:
        print("任務失敗。")