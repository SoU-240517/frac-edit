import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("マンデルブロ集合描画アプリ")
        master.geometry("1400x900")
        self.create_widgets()

    def create_widgets(self):
        # --- メインフレーム ---
        self.main_frame = tk.Frame(self.master, bg="white")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # --- 左: コンテンツ領域 / 右: 操作パネル ---
        self.content_area = tk.Frame(self.main_frame, bg="white")
        self.control_panel = tk.Frame(self.main_frame, bg="lightgray", width=250)
        self.content_area.grid(row=0, column=0, sticky="nsew")
        self.control_panel.grid(row=0, column=1, sticky="ns")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # === 操作パネル内のウィジェット（上から順に配置） ===
        # 1. キャンバスビュー（仮でテキストボックスを配置）
        self.g_view_text = tk.Text(self.control_panel, wrap=tk.WORD, width=20, height=11)
        self.g_view_text.grid(row=0, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        self.g_view_text.insert("1.0", "仮でテキストボックスを配置\n本来は、キャンバスのミニマップを表示する")
        self.g_view_text.config(state="disabled")

        # 2. キャンバス／ノード切替ボタン
        self.toggle_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.toggle_frame.grid(row=1, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        self.canvas_button = tk.Button(self.toggle_frame, text="キャンバス")
        self.canvas_button.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.node_button = tk.Button(self.toggle_frame, text="ノード編集")
        self.node_button.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.toggle_frame.columnconfigure(0, weight=1)
        self.toggle_frame.columnconfigure(1, weight=1)

        # 3. パラメータセーブ／ロードボタン
        self.save_load_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.save_load_frame.grid(row=2, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        self.param_save_button = tk.Button(self.save_load_frame, text="パラメータセーブ")
        self.param_save_button.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.param_load_button = tk.Button(self.save_load_frame, text="パラメータロード")
        self.param_load_button.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.save_load_frame.columnconfigure(0, weight=1)
        self.save_load_frame.columnconfigure(1, weight=1)

        # 4. ズーム倍率／感度設定
        self.zoom_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.zoom_frame.grid(row=3, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        self.zoom_bairitu_label = tk.Label(self.zoom_frame, text="ズーム倍率:", width=8)
        self.zoom_bairitu_label.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.zoom_bairitu_entry = ttk.Entry(self.zoom_frame, width=10)
        self.zoom_bairitu_entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.zoom_bairitu_entry.insert(0, "1.0")
        self.zoom_kando_label = tk.Label(self.zoom_frame, text="ズーム感度:", width=8)
        self.zoom_kando_label.grid(row=0, column=2, padx=3, pady=3, sticky="w")
        self.zoom_kando_entry = ttk.Entry(self.zoom_frame, width=10)
        self.zoom_kando_entry.grid(row=0, column=3, padx=3, pady=3, sticky="ew")
        self.zoom_kando_entry.insert(0, "1.0")
        self.zoom_frame.columnconfigure(1, weight=1)
        self.zoom_frame.columnconfigure(3, weight=1)

        # 5. フレーム選択＆追加
        self.myframe_select_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.myframe_select_frame.grid(row=4, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        self.myframe_dropdown = tk.StringVar(self.master)
        self.myframe_dropdown.set("フレーム選択")
        self.myframe_values = ["フレーム1"]
        self.frame_dropdown = ttk.Combobox(self.myframe_select_frame, textvariable=self.myframe_dropdown,
                                           values=self.myframe_values)
        self.frame_dropdown.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.add_myframe_button = tk.Button(self.myframe_select_frame, text="+", width=2, command=self.add_frame)
        self.add_myframe_button.grid(row=0, column=1, padx=3, pady=3)
        self.myframe_select_frame.columnconfigure(0, weight=1)
        self.myframe_dropdown.trace_add("write", self.update_listbox)

        # 6. フラクタルタイプ選択
        self.frac_type_dropdown = tk.StringVar(self.master)
        self.frac_type_dropdown.set("フラクタルタイプ")
        self.frac_type_combobox = ttk.Combobox(self.control_panel, textvariable=self.frac_type_dropdown,
                                               values=["Julia/Mandelbrot", "Linear", "TEST1", "TEST2"])
        self.frac_type_combobox.grid(row=5, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        self.frac_type_dropdown.trace_add("write", self.update_listbox)

        # 7. Treeview（フレーム＆フラクタルタイプ表示）
        self.tree = ttk.Treeview(self.control_panel, columns=("frame", "ftype"), show="headings", height=5)
        self.tree.heading("frame", text="フレーム選択")
        self.tree.heading("ftype", text="フラクタルタイプ")
        self.tree.column("frame", width=100, anchor="center")
        self.tree.column("ftype", width=100, anchor="center")
        self.tree.grid(row=6, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        self.update_listbox()

        # 8. プラグイン領域①（漸化式と反復回数）
        self.plugin_frame1 = tk.Frame(self.control_panel, bg="darkgray")
        self.plugin_frame1.grid(row=7, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        # 漸化式入力
        self.zanka_frame = tk.Frame(self.plugin_frame1, bg="lightblue")
        self.zanka_frame.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        zanka_label = tk.Label(self.zanka_frame, text="漸化式:", bg="lightgreen", width=15)
        zanka_label.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.zanka_entry = ttk.Entry(self.zanka_frame, width=50)
        self.zanka_entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.zanka_frame.columnconfigure(1, weight=1)
        # 反復回数入力
        self.hanpuku_frame = tk.Frame(self.plugin_frame1, bg="lightblue")
        self.hanpuku_frame.grid(row=1, column=0, padx=3, pady=3, sticky="ew")
        hanpuku_label = tk.Label(self.hanpuku_frame, text="反復回数:", bg="lightgreen", width=15)
        hanpuku_label.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.hanpuku_entry = ttk.Entry(self.hanpuku_frame, width=50)
        self.hanpuku_entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.hanpuku_frame.columnconfigure(1, weight=1)

        # 9. プラグイン領域②（Z/C入力）
        self.plugin_frame2 = tk.Frame(self.control_panel, bg="darkgray")
        self.plugin_frame2.grid(row=8, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        # Z-実・Z-虚入力
        self.z_frame = tk.Frame(self.plugin_frame2, bg="lightblue")
        self.z_frame.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        z_real_label = tk.Label(self.z_frame, text="Z-実:", bg="lightgreen", width=5)
        z_real_label.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.z_real_entry = ttk.Entry(self.z_frame, width=26)
        self.z_real_entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        z_imag_label = tk.Label(self.z_frame, text="Z-虚:", bg="lightgreen", width=5)
        z_imag_label.grid(row=0, column=2, padx=3, pady=3, sticky="w")
        self.z_imag_entry = ttk.Entry(self.z_frame, width=26)
        self.z_imag_entry.grid(row=0, column=3, padx=3, pady=3, sticky="ew")
        self.z_frame.columnconfigure(1, weight=1)
        self.z_frame.columnconfigure(3, weight=1)
        # C-実・C-虚入力
        self.c_frame = tk.Frame(self.plugin_frame2, bg="lightblue")
        self.c_frame.grid(row=1, column=0, padx=3, pady=3, sticky="ew")
        c_real_label = tk.Label(self.c_frame, text="C-実:", bg="lightgreen", width=5)
        c_real_label.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.c_real_entry = ttk.Entry(self.c_frame)
        self.c_real_entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        c_imag_label = tk.Label(self.c_frame, text="C-虚:", bg="lightgreen", width=5)
        c_imag_label.grid(row=0, column=2, padx=3, pady=3, sticky="w")
        self.c_imag_entry = ttk.Entry(self.c_frame)
        self.c_imag_entry.grid(row=0, column=3, padx=3, pady=3, sticky="ew")
        self.c_frame.columnconfigure(1, weight=1)
        self.c_frame.columnconfigure(3, weight=1)

        # 10. 色設定領域
        self.color_set_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.color_set_frame.grid(row=9, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")
        self.color_set_frame.columnconfigure(0, weight=1)
        self.color_set_frame.columnconfigure(1, weight=1)
        # グラデーションロード
        self.grad_load_button = tk.Button(self.color_set_frame, text="グラデーションロード")
        self.grad_load_button.grid(row=0, column=0, columnspan=2, padx=3, pady=3, sticky="ew")
        # 発散領域の色設定
        self.color_hassan_frame = tk.Frame(self.color_set_frame, bg="lightblue")
        self.color_hassan_frame.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky="ew")
        hassan_label_frame = tk.Frame(self.color_hassan_frame, bg="lightgreen")
        hassan_label_frame.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        hassan_algo_label = tk.Label(hassan_label_frame, text="発散:", bg="yellow", width=8)
        hassan_algo_label.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.hassan_algo_dropdown = tk.StringVar(self.master)
        self.hassan_algo_dropdown.set("アルゴリズム1")
        self.hassan_algo_values = ["アルゴリズム1", "アルゴリズム2", "アルゴリズム3"]
        self.hassan_algo_combobox = ttk.Combobox(hassan_label_frame,
                                                 textvariable=self.hassan_algo_dropdown,
                                                 values=self.hassan_algo_values, width=15)
        self.hassan_algo_combobox.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.hassan_grad_radio_var = tk.IntVar(value=0)
        self.hassan_grad_radio = tk.Radiobutton(self.color_hassan_frame,
                                                variable=self.hassan_grad_radio_var,
                                                value=1, bg="lightgreen")
        self.hassan_grad_radio.grid(row=0, column=1, padx=3, pady=3, sticky="e")
        self.hassan_grad_dropdown = tk.StringVar(self.master)
        self.hassan_grad_dropdown.set("グラデーション1")
        self.hassan_grad_dropdown_values = ["グラデーション1", "グラデーション2", "グラデーション3", "グラデーション4", "グラデーション5"]
        self.hassan_grad_combobox = ttk.Combobox(self.color_hassan_frame,
                                                 textvariable=self.hassan_grad_dropdown,
                                                 values=self.hassan_grad_dropdown_values)
        self.hassan_grad_combobox.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky="ew")
        # 非発散領域の色設定
        self.color_non_hassan_frame = tk.Frame(self.color_set_frame, bg="lightblue")
        self.color_non_hassan_frame.grid(row=2, column=0, columnspan=2, padx=3, pady=3, sticky="ew")
        non_hassan_label_frame = tk.Frame(self.color_non_hassan_frame, bg="lightgreen")
        non_hassan_label_frame.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        non_hassan_algo_label = tk.Label(non_hassan_label_frame, text="非発散:", bg="yellow", width=8)
        non_hassan_algo_label.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.non_hassan_algo_dropdown = tk.StringVar(self.master)
        self.non_hassan_algo_dropdown.set("アルゴリズムA")
        self.non_hassan_algo_values = ["アルゴリズムA", "アルゴリズムB", "アルゴリズムC"]
        self.non_hassan_algo_combobox = ttk.Combobox(non_hassan_label_frame,
                                                     textvariable=self.non_hassan_algo_dropdown,
                                                     values=self.non_hassan_algo_values, width=15)
        self.non_hassan_algo_combobox.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.non_hassan_grad_radio_var = tk.IntVar(value=0)
        self.non_hassan_grad_radio = tk.Radiobutton(self.color_non_hassan_frame,
                                                    variable=self.non_hassan_grad_radio_var,
                                                    value=1, bg="lightgreen")
        self.non_hassan_grad_radio.grid(row=0, column=1, padx=3, pady=3, sticky="e")
        self.non_hassan_grad_dropdown = tk.StringVar(self.master)
        self.non_hassan_grad_dropdown.set("グラデーション1")
        self.non_hassan_grad_dropdown_values = ["グラデーション1", "グラデーション2", "グラデーション3", "グラデーション4", "グラデーション5"]
        self.non_hassan_grad_combobox = ttk.Combobox(self.color_non_hassan_frame,
                                                     textvariable=self.non_hassan_grad_dropdown,
                                                     values=self.non_hassan_grad_dropdown_values)
        self.non_hassan_grad_combobox.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky="ew")

        # 11. 作品描画ボタン
        self.draw_button = tk.Button(self.control_panel, text="作品描画")
        self.draw_button.grid(row=10, column=0, columnspan=2, padx=3, pady=(3,0), sticky="ew")

        # === コンテンツ領域内のウィジェット ===

        # マンデルブロ集合表示ラベル
        content_label = tk.Label(self.content_area, text="ここにマンデルブロ集合を表示", bg="white")
        content_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        # メッセージ表示ラベル
        self.message_label = tk.Label(self.content_area, text="ここにメッセージを表示します",
                                       bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="white")
        self.message_label.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        # グラデーション編集領域
        self.gradient_frame = tk.Frame(self.content_area, bd=1, relief=tk.SUNKEN, bg="lightgray")
        self.gradient_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        left_frame = tk.Frame(self.gradient_frame, bg="white")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.gradient_frame.grid_columnconfigure(0, weight=1)
        self.grad_txt1 = tk.Label(left_frame, text="グラデーション編集（仮）メッセージ1", anchor=tk.W, bg="white")
        self.grad_txt1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.grad_txt2 = tk.Label(left_frame, text="グラデーション編集（仮）メッセージ2", anchor=tk.W, bg="white")
        self.grad_txt2.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.grad_txt3 = tk.Label(left_frame, text="グラデーション編集（仮）メッセージ3", anchor=tk.W, bg="white")
        self.grad_txt3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        right_frame = tk.Frame(self.gradient_frame, bg="white")
        right_frame.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
        self.save_button = tk.Button(right_frame, text="グラデーションセーブ")
        self.save_button.grid(row=0, column=0, padx=5, pady=5)

        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

    def update_listbox(self, *args):
        self.tree.delete(*self.tree.get_children())
        frame_selection = self.myframe_dropdown.get()
        ftype_selection = self.frac_type_dropdown.get()
        self.tree.insert("", tk.END, values=(frame_selection, ftype_selection))

    def add_frame(self):
        new_frame_name = "フレーム" + str(len(self.myframe_values) + 1)
        self.myframe_values.append(new_frame_name)
        self.frame_dropdown["values"] = self.myframe_values
        self.myframe_dropdown.set(new_frame_name)
        self.update_listbox()

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
