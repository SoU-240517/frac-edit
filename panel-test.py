import tkinter as tk
import tkinter.ttk as ttk  # 改善されたウィジェットのために追加

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("マンデルブロ集合描画アプリ")

        # ウィンドウサイズを設定（フルスクリーンではなくなる）
        master.geometry("800x600")  # 例：幅800ピクセル、高さ600ピクセル

        self.create_widgets()

    def create_widgets(self):
        """ウィジェットを作成する"""

        # メインフレーム
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 操作パネルフレーム（右側）
        self.control_panel = tk.Frame(self.main_frame, bg="lightgray", width=250)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        # 操作パネルのタイトル
        title_label = tk.Label(self.control_panel, text="操作パネル", bg="lightgray")
        title_label.pack(pady=1)

        # --- キャンバス/ノード編集 切替ボタン ---
        node_frame = tk.Frame(self.control_panel, bg="lightgray")  # ボタンを格納するフレーム
        node_frame.pack(pady=1, padx=1)

        self.draw_button1 = tk.Button(node_frame, text="キャンバス")
        self.draw_button1.pack(side=tk.LEFT, padx=(0,20))

        self.draw_button2 = tk.Button(node_frame, text="ノード編集")
        self.draw_button2.pack(side=tk.LEFT)

        # --- 漸化式入力フィールド ---
        zanka_frame = tk.Frame(self.control_panel, bg="lightgray")
        zanka_frame.pack(pady=(5, 0), padx=10, fill=tk.X)
        recurrence_label = tk.Label(zanka_frame, text="漸化式:", bg="lightgray")
        recurrence_label.pack(side=tk.LEFT)
        self.recurrence_entry = ttk.Entry(zanka_frame)
        self.recurrence_entry.pack(side=tk.LEFT, padx=(12, 5), fill=tk.X)

        # --- 反復回数入力フィールド ---
        hanpuku_frame = tk.Frame(self.control_panel, bg="lightgray")
        hanpuku_frame.pack(pady=(5, 0), padx=10, fill=tk.X)
        iteration_label = tk.Label(hanpuku_frame, text="反復回数:", bg="lightgray")
        iteration_label.pack(side=tk.LEFT)
        self.iteration_entry = ttk.Entry(hanpuku_frame)
        self.iteration_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X)

        # --- Z-実 / Z-虚 入力フィールド ---
        z_frame = tk.Frame(self.control_panel, bg="lightgray")
        z_frame.pack(pady=(10, 0), padx=10, fill=tk.X)

        z_real_label = tk.Label(z_frame, text="Z-実:", bg="lightgray")
        z_real_label.pack(side=tk.LEFT)
        self.z_real_entry = ttk.Entry(z_frame)
        self.z_real_entry.pack(side=tk.LEFT, padx=(0,5), fill=tk.X, expand=True)

        z_imag_label = tk.Label(z_frame, text="Z-虚:", bg="lightgray")
        z_imag_label.pack(side=tk.LEFT)
        self.z_imag_entry = ttk.Entry(z_frame)
        self.z_imag_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- C-実 / C-虚 入力フィールド ---
        c_frame = tk.Frame(self.control_panel, bg="lightgray")
        c_frame.pack(pady=(10, 0), padx=10, fill=tk.X)

        c_real_label = tk.Label(c_frame, text="C-実:", bg="lightgray")
        c_real_label.pack(side=tk.LEFT)
        self.c_real_entry = ttk.Entry(c_frame)
        self.c_real_entry.pack(side=tk.LEFT, padx=(0,5), fill=tk.X, expand=True)

        c_imag_label = tk.Label(c_frame, text="C-虚:", bg="lightgray")
        c_imag_label.pack(side=tk.LEFT)
        self.c_imag_entry = ttk.Entry(c_frame)
        self.c_imag_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- 作品描画ボタン ---
        self.draw_button = tk.Button(self.control_panel, text="作品描画")
        self.draw_button.pack(pady=10)

        # --- リストボックス ---
        self.listbox = tk.Listbox(self.control_panel)
        self.listbox.pack(pady=10, padx=10, fill=tk.X)
        # リストボックスにテスト項目を追加
        for i in range(5):
            self.listbox.insert(tk.END, f"item{i}")

        # --- ドロップダウンリスト ---
        self.dropdown_var = tk.StringVar(self.master)
        self.dropdown_var.set("選択肢1")  # デフォルト値を設定
        self.dropdown = ttk.Combobox(self.control_panel, textvariable=self.dropdown_var, values=["選択肢1", "選択肢2", "選択肢3"])
        self.dropdown.pack(pady=10, padx=10, fill=tk.X)


        # --- スライダー ---
        self.slider_var = tk.DoubleVar()
        self.slider = tk.Scale(self.control_panel, variable=self.slider_var, from_=0, to=100, orient=tk.HORIZONTAL, label="スライダー")
        self.slider.pack(pady=10, padx=10, fill=tk.X)

        # メインコンテンツ領域（左側）
        self.content_area = tk.Frame(self.main_frame)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 例としてラベルを配置
        content_label = tk.Label(self.content_area, text="ここにマンデルブロ集合を表示")
        content_label.pack()

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
