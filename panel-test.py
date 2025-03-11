import tkinter as tk
import tkinter.ttk as ttk

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

        # ---  改行できるテキストボックス★仮★（本当は、キャンバス部分のミニマップを配置する ---
        self.description_text = tk.Text(self.control_panel, wrap=tk.WORD, width=240, height=9)  #16:9になるように高さを調整
        self.description_text.pack(pady=(5, 0), padx=5, fill=tk.X)
        self.description_text.config(width=20)  #240 / 12 = 20
        self.description_text.config(height=11)# 9 * 16 / 9=16　文字の高さ(1文字あたり)1.4を想定　16 / 1.4 = 11.42  切り捨てで11
        #--- 初期テキストを挿入
        self.description_text.insert("1.0", "仮でテキストボックスを配置\n本来は、キャンバスのミニマップを表示する")
        self.description_text.config(state="disabled") #編集不可にする

        # --- キャンバス/ノード編集 切替ボタン ---
        canvas_chenge_frame = tk.Frame(self.control_panel, bg="lightgray")  # ボタンを格納するフレーム
        canvas_chenge_frame.pack(pady=(5, 0), padx=1)

        self.canvas_button = tk.Button(canvas_chenge_frame, text="キャンバス")
        self.canvas_button.pack(side=tk.LEFT, padx=(0, 20))

        self.node_button = tk.Button(canvas_chenge_frame, text="ノード編集")
        self.node_button.pack(side=tk.LEFT)

        # --- フレーム選択ドロップダウンリスト + 追加ボタン ---
        myframe_select_frame = tk.Frame(self.control_panel, bg="lightgray")
        myframe_select_frame.pack(pady=(5, 0), padx=10, fill=tk.X)

        self.myframe_dropdown = tk.StringVar(self.master)
        self.myframe_dropdown.set("フレーム選択")  # デフォルト値を設定
        self.frame_values = ["フレーム1"]  # ドロップダウンの選択肢をリストで管理
        self.dropdown = ttk.Combobox(myframe_select_frame, textvariable=self.myframe_dropdown, values=self.frame_values)
        self.dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.myframe_dropdown.trace_add("write", self.update_listbox)

        self.add_myframe_button = tk.Button(myframe_select_frame, text="+", width=2, command=self.add_frame)
        self.add_myframe_button.pack(side=tk.LEFT, padx=(5,0))

        # --- フラクタルタイプドロップダウンリスト ---
        self.frac_type_dropdown = tk.StringVar(self.master)
        self.frac_type_dropdown.set("フラクタルタイプ")  # デフォルト値を設定
        self.dropdown2 = ttk.Combobox(self.control_panel, textvariable=self.frac_type_dropdown, values=["Julia/Mandelbrot", "Linear", "TEST1", "TEST2"])
        self.dropdown2.pack(pady=(5, 0), padx=10, fill=tk.X)
        self.frac_type_dropdown.trace_add("write", self.update_listbox)

        # --- リストボックス（Treeviewを使用）---
        self.tree = ttk.Treeview(self.control_panel, columns=("frame", "ftype"), show="headings", height=5)
        self.tree.heading("frame", text="フレーム選択")
        self.tree.heading("ftype", text="フラクタルタイプ")
        self.tree.column("frame", width=100)
        self.tree.column("ftype", width=100)
        self.tree.pack(pady=10, padx=10, fill=tk.X)
        self.update_listbox() #リストボックスの初期化のために呼び出し

        # --- プラグインフィールド１　漸化式と反復回数入力フィールドをまとめたフレーム ---
        plugin_fields1_frame = tk.Frame(self.control_panel, bg="lightgray")
        plugin_fields1_frame.pack(pady=(5, 0), padx=10, fill=tk.X)

        # --- 漸化式入力フィールド ---
        zanka_frame = tk.Frame(plugin_fields1_frame, bg="lightgray")
        zanka_frame.pack(fill=tk.X)

        recurrence_label = tk.Label(zanka_frame, text="漸化式:", bg="lightgray")
        recurrence_label.pack(side=tk.LEFT)

        self.recurrence_entry = ttk.Entry(zanka_frame, width=45)
        self.recurrence_entry.pack(side=tk.LEFT, padx=(12, 0), fill=tk.X)

        # --- 反復回数入力フィールド ---
        hanpuku_frame = tk.Frame(plugin_fields1_frame, bg="lightgray")
        hanpuku_frame.pack(fill=tk.X)

        iteration_label = tk.Label(hanpuku_frame, text="反復回数:", bg="lightgray")
        iteration_label.pack(side=tk.LEFT)

        self.iteration_entry = ttk.Entry(hanpuku_frame, width=45)
        self.iteration_entry.pack(side=tk.LEFT, fill=tk.X)

        # --- プラグインフィールド２　Z/C 入力フィールドをまとめたフレーム ---
        plugin_fields2_frame = tk.Frame(self.control_panel, bg="lightgray")
        plugin_fields2_frame.pack(pady=(5, 0), padx=10, fill=tk.X)

        # --- Z-実 / Z-虚 入力フィールド ---
        z_frame = tk.Frame(plugin_fields2_frame, bg="lightgray")
        z_frame.pack(fill=tk.X)

        z_real_label = tk.Label(z_frame, text="Z-実:", bg="lightgray")
        z_real_label.pack(side=tk.LEFT)

        self.z_real_entry = ttk.Entry(z_frame)
        self.z_real_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        z_imag_label = tk.Label(z_frame, text="Z-虚:", bg="lightgray")
        z_imag_label.pack(side=tk.LEFT)

        self.z_imag_entry = ttk.Entry(z_frame)
        self.z_imag_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- C-実 / C-虚 入力フィールド ---
        c_frame = tk.Frame(plugin_fields2_frame, bg="lightgray")
        c_frame.pack(fill=tk.X)

        c_real_label = tk.Label(c_frame, text="C-実:", bg="lightgray")
        c_real_label.pack(side=tk.LEFT)

        self.c_real_entry = ttk.Entry(c_frame)
        self.c_real_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        c_imag_label = tk.Label(c_frame, text="C-虚:", bg="lightgray")
        c_imag_label.pack(side=tk.LEFT)

        self.c_imag_entry = ttk.Entry(c_frame)
        self.c_imag_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- 作品描画ボタン ---
        self.draw_button = tk.Button(self.control_panel, text="作品描画")
        self.draw_button.pack(pady=5)

        # メインコンテンツ領域（左側）
        self.content_area = tk.Frame(self.main_frame)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # メッセージ表示欄を追加
        self.message_label = tk.Label(self.content_area, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.message_label.config(text="ここにメッセージを表示します")
        self.message_label.pack(side=tk.BOTTOM, fill=tk.X)

        # 例としてラベルを配置
        content_label = tk.Label(self.content_area, text="ここにマンデルブロ集合を表示")
        content_label.pack()

    def update_listbox(self, *args):
        """リストボックスの内容を更新する"""
        self.tree.delete(*self.tree.get_children())  # 既存のアイテムをすべて削除
        frame_selection = self.myframe_dropdown.get()
        ftype_selection = self.frac_type_dropdown.get()
        self.tree.insert("", tk.END, values=(frame_selection, ftype_selection))
        #リストボックスに値が一つだけ入るようにしているので、複数個入れたい場合は以下を参考に
        #for i in range(5):
        #    self.tree.insert("", tk.END, values=(f"frame{i}", f"ftype{i}"))

    def add_frame(self):
        """フレームを追加する"""
        new_frame_name = "フレーム" + str(len(self.frame_values) + 1)
        self.frame_values.append(new_frame_name)  # 選択肢リストに追加
        self.dropdown["values"] = self.frame_values  # ドロップダウンを更新
        self.myframe_dropdown.set(new_frame_name)  # 新しいフレームを選択済みにする
        self.update_listbox() #リストボックスの更新

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
