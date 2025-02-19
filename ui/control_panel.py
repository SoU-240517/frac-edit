# julia_viewer/ui/control_panel.py
import tkinter as tk
from tkinter import ttk
from core import color_map # color_mapモジュールのインポート

class ControlPanel(ttk.Frame):
    def __init__(self, parent, main_window): # main_windowを引数として受け取る
        super().__init__(parent, padding="10")
        self.main_window = main_window # MainWindowインスタンスを保持
        self.setup_panel()

    def setup_panel(self):
        # 実部のコントロール
        ttk.Label(self, text="実部:").pack()
        real_entry = ttk.Entry(self, textvariable=self.main_window.real, width=20) # MainWindowの変数を参照
        real_entry.pack()
        real_entry.bind('<Return>', self.on_entry_change)
        real_entry.bind('<FocusOut>', self.on_entry_change)
        real_slider = ttk.Scale(self, from_=-2.0, to=2.0, variable=self.main_window.real, # MainWindowの変数を参照
                                    orient=tk.HORIZONTAL, command=self.on_slider_change_real) # スライダー変更時イベント

        real_slider.pack()

        # 虚部のコントロール
        ttk.Label(self, text="虚部:").pack()
        imag_entry = ttk.Entry(self, textvariable=self.main_window.imag, width=20) # MainWindowの変数を参照
        imag_entry.pack()
        imag_entry.bind('<Return>', self.on_entry_change)
        imag_entry.bind('<FocusOut>', self.on_entry_change)
        imag_slider = ttk.Scale(self, from_=-2.0, to=2.0, variable=self.main_window.imag, # MainWindowの変数を参照
                                    orient=tk.HORIZONTAL, command=self.on_slider_change_imag) # スライダー変更時イベント
        imag_slider.pack()

        # 反復回数のコントロール
        ttk.Label(self, text="反復回数:").pack()
        iter_entry = ttk.Entry(self, textvariable=self.main_window.max_iter, width=10) # MainWindowの変数を参照
        iter_entry.pack()
        iter_entry.bind('<Return>', self.on_iter_change)  # Enterキーで更新
        iter_entry.bind('<FocusOut>', self.on_iter_change)  # フォーカスを失ったときに更新

        # カラーマップのコントロール
        ttk.Label(self, text="開始色:").pack()
        color_frame1 = ttk.Frame(self)
        color_frame1.pack(fill=tk.X, pady=2)

        start_color_entry = ttk.Entry(color_frame1, textvariable=self.main_window.start_color, width=8) # MainWindowの変数を参照
        start_color_entry.pack(side=tk.LEFT, padx=2)
        start_color_entry.bind('<Return>', self.on_color_change_start)
        start_color_entry.bind('<FocusOut>', self.on_color_change_start)

        ttk.Button(color_frame1, text="選択",
                         command=lambda: self.choose_color('start')).pack(side=tk.LEFT)

        ttk.Label(self, text="終了色:").pack()
        color_frame2 = ttk.Frame(self)
        color_frame2.pack(fill=tk.X, pady=2)

        end_color_entry = ttk.Entry(color_frame2, textvariable=self.main_window.end_color, width=8) # MainWindowの変数を参照
        end_color_entry.pack(side=tk.LEFT, padx=2)
        end_color_entry.bind('<Return>', self.on_color_change_end)
        end_color_entry.bind('<FocusOut>', self.on_color_change_end)

        ttk.Button(color_frame2, text="選択",
                         command=lambda: self.choose_color('end')).pack(side=tk.LEFT)

        # 更新ボタン
        ttk.Button(self, text="更新", command=self.full_draw).pack(pady=10)

        # リセットボタンの追加
        ttk.Button(self, text="リセット", command=self.reset_params).pack(pady=10)


    # --- イベントハンドラ (コントロールパネル) ---
    def on_slider_change_real(self, value):
        try:
            real_val = float(value)
            self.main_window.set_real_param(real_val) # MainWindowのパラメータ設定関数を呼び出す
        except ValueError:
            pass # スライダーの値が数値に変換できない場合は何もしない

    def on_slider_change_imag(self, value):
        try:
            imag_val = float(value)
            self.main_window.set_imag_param(imag_val) # MainWindowのパラメータ設定関数を呼び出す
        except ValueError:
            pass # スライダーの値が数値に変換できない場合は何もしない


    def on_entry_change(self, event):
        try:
            # 入力値を検証
            real_val = float(self.main_window.real.get())
            imag_val = float(self.main_window.imag.get())

            # 値の範囲を制限
            self.main_window.set_real_param(max(-2.0, min(2.0, real_val))) # MainWindowのパラメータ設定関数を呼び出す
            self.main_window.set_imag_param(max(-2.0, min(2.0, imag_val))) # MainWindowのパラメータ設定関数を呼び出す

        except ValueError:
            # 無効な入力の場合は以前の値に戻す (エントリーの値は StringVar で管理しているので、ここでは何もしない)
            pass

    def on_iter_change(self, event):
        try:
            # 入力値を検証
            iter_val = int(self.main_window.max_iter.get())

            # 最小値を1に制限
            self.main_window.set_max_iter_param(max(1, iter_val)) # MainWindowのパラメータ設定関数を呼び出す

        except ValueError:
            # 無効な入力の場合は以前の値に戻す (エントリーの値は StringVar で管理しているので、ここでは何もしない)
            pass

    def on_color_change_start(self, event):
        start_color = self.main_window.start_color.get()
        if not color_map.is_valid_hex_color(start_color): # color_mapモジュールの関数を使用
            self.main_window.set_start_color_param("#0000FF") # デフォルトの開始色

    def on_color_change_end(self, event):
        end_color = self.main_window.end_color.get()
        if not color_map.is_valid_hex_color(end_color): # color_mapモジュールの関数を使用
            self.main_window.set_end_color_param("#FFFFFF") # デフォルトの終了色


    def choose_color(self, color_type):
        """カラーパレットを表示して色を選択"""
        current_color = self.main_window.start_color.get() if color_type == 'start' else self.main_window.end_color.get()
        title = f"{color_type.capitalize()}色の選択"
        selected_color = color_map.choose_color(self, current_color, title) # color_mapモジュールの関数を使用

        if selected_color:  # 色が選択された場合
            if color_type == 'start':
                self.main_window.set_start_color_param(selected_color) # MainWindowのパラメータ設定関数を呼び出す
            else:
                self.main_window.set_end_color_param(selected_color) # MainWindowのパラメータ設定関数を呼び出す


    def full_draw(self):
        self.main_window.full_draw() # MainWindowの描画関数を呼び出す

    def reset_params(self):
        self.main_window.reset_params() # MainWindowのリセット関数を呼び出す
