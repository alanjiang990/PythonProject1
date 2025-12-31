import sys
import sqlite3
import pandas as pd
import math
import datetime
import csv
import subprocess
import os
import translate_csv

# 1. 先引入 PyQt6，確保環境以此為優先
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QFileDialog, QLabel, QHBoxLayout,QGroupBox,QLineEdit)

# 2. 設定 Matplotlib 使用 QtAgg 後端 (有時候這行非必要，但在出錯時很有用)
import matplotlib
matplotlib.use('QtAgg')

# 3. 最後再引入 pyplot 和 canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class MplCanvas(FigureCanvas):
    """這是一個畫布物件，專門用來在 PyQt 裡顯示 Matplotlib 圖表"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(fig)


class DataProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("混合式資料載入系統")
        self.resize(900, 700)

        # 【狀態管理】
        self.db_path = None  # 存：後台算好的軌跡 DB 路徑
        self.special_csv_path = None  # 存：使用者選的特殊點 CSV 原始路徑

        # --- UI 配置 (跟上一次一樣，沒變) ---
        main_layout = QVBoxLayout()
        input_group = QGroupBox("資料來源")
        input_layout = QVBoxLayout()

        # 軌跡輸入
        layout_a = QHBoxLayout()
        self.line_traj = QLineEdit()
        btn_browse_traj = QPushButton("瀏覽軌跡 CSV...")
        btn_browse_traj.clicked.connect(lambda: self.browse_file(self.line_traj))
        layout_a.addWidget(self.line_traj)
        layout_a.addWidget(btn_browse_traj)

        # 特殊點輸入
        layout_b = QHBoxLayout()
        self.line_special = QLineEdit()
        btn_browse_special = QPushButton("瀏覽特殊點 CSV...")
        btn_browse_special.clicked.connect(lambda: self.browse_file(self.line_special))
        layout_b.addWidget(self.line_special)
        layout_b.addWidget(btn_browse_special)

        input_layout.addLayout(layout_a)
        input_layout.addLayout(layout_b)
        input_group.setLayout(input_layout)

        self.btn_run = QPushButton("執行處理與繪圖")
        self.btn_run.clicked.connect(self.start_processing)
        self.status_label = QLabel("狀態：等待輸入")
        self.canvas = MplCanvas(self)

        main_layout.addWidget(input_group)
        main_layout.addWidget(self.btn_run)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def browse_file(self, line_edit):
        path, _ = QFileDialog.getOpenFileName(self, "選擇檔案", "", "CSV Files (*.csv)")
        if path: line_edit.setText(path)

    # --- 核心邏輯：分流處理 ---
    def start_processing(self):
        traj_path = self.line_traj.text()
        special_path = self.line_special.text()

        if not traj_path:
            self.status_label.setText("錯誤：必須選擇軌跡檔案")
            return

        self.status_label.setText("狀態：後台正在轉換 DB，特殊點準備直接讀取...")
        QApplication.processEvents()

        try:
            # 1. 【重活】丟給後台：軌跡轉 DB
            # 這裡我們只傳 traj_path，後台只回傳 db_path
            self.db_path = translate_csv.convert_csv_to_db(traj_path)

            # 2. 【輕活】自己記住：特殊點 CSV 路徑
            # 我們直接把路徑存進變數，等一下畫圖直接讀這個檔案
            self.special_csv_path = special_path if os.path.exists(special_path) else None

            self.status_label.setText("處理完成！正在混合繪製...")

            # 3. 呼叫繪圖
            self.update_plot_hybrid()

        except Exception as e:
            self.status_label.setText(f"執行錯誤：{str(e)}")

    # --- 繪圖邏輯：混合讀取 (DB + CSV) ---
    def update_plot_hybrid(self):
        self.canvas.figure.clear()
        self.axes = self.canvas.figure.add_subplot(111)

        # --- 來源 A: 從 DB 讀取軌跡 ---
        if self.db_path and os.path.exists(self.db_path):
            try:
                conn = sqlite3.connect(self.db_path)
                df_traj = pd.read_sql("SELECT * FROM points", conn)
                conn.close()

                if 'x' in df_traj.columns and 'y' in df_traj.columns:
                    c_data = range(len(df_traj))
                    sc = self.axes.scatter(
                        df_traj['x'], df_traj['y'], c=c_data, cmap='jet',
                        s=50, edgecolors='k', linewidth=0.5, alpha=0.7, label='Trajectory (DB)'
                    )
                    self.axes.plot(df_traj['x'], df_traj['y'], color='gray', alpha=0.3, linestyle='--')
                    self.canvas.figure.colorbar(sc, ax=self.axes, label="Sequence")
            except Exception as e:
                print(f"DB讀取錯誤: {e}")

        # --- 來源 B: 直接從 CSV 讀取特殊點 ---
        # 這裡就是你要的：不經過後台，直接讀原本的檔案
        if self.special_csv_path and os.path.exists(self.special_csv_path):
            try:
                # 直接用 Pandas 讀 CSV
                df_special = pd.read_csv(self.special_csv_path)

                if 'x' in df_special.columns and 'y' in df_special.columns:
                    self.axes.scatter(
                        df_special['x'], df_special['y'],
                        color='red', marker='*', s=300,
                        edgecolors='black', linewidth=1.5,
                        label='Special Points (CSV)', zorder=10
                    )
            except Exception as e:
                print(f"CSV讀取錯誤: {e}")

        # 通用設定
        self.axes.set_title("Hybrid Visualization (DB + CSV)")
        self.axes.set_xlabel("X")
        self.axes.set_ylabel("Y")
        self.axes.grid(True)
        self.axes.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataProcessorApp()
    window.show()
    sys.exit(app.exec())