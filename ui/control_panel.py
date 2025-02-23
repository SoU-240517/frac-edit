import tkinter as tk # Tkinterのインポート
from tkinter import ttk # ttkモジュールのインポート
from core import color_map # color_mapモジュールのインポート

# ControlPanelクラスの定義
class ControlPanel(ttk.Frame):
    # コンストラクタ
    def __init__(self, parent, main_window): # main_windowを引数として受け取る
        super().__init__(parent, padding="10") # 親クラスのコンストラクタを呼び出す
        self.main_window = main_window # MainWindowインスタンスを保持
        self.setup_panel() # パネルのセットアップ

    # パネルのセットアップ
    def setup_panel(self):
        # 実部のコントロール
        ttk.Label(self, text="実部:").pack() # ラベルを配置
        vcmd = (self.register(self.validate_real), '%P') # 入力値を検証する関数を登録
        real_entry = ttk.Entry(self, textvariable=self.main_window.real, width=20, validate='key', validatecommand=vcmd) # MainWindowの変数を参照
        real_entry.pack() # エントリーを配置
        real_entry.bind('<Return>', self.on_entry_change) # Enterキーで更新
        real_entry.bind('<FocusOut>', self.on_entry_change) # フォーカスを失ったときに更新
        real_slider = ttk.Scale(self, from_=-2.0, to=2.0, variable=self.main_window.real, # MainWindowの変数を参照
                                    orient=tk.HORIZONTAL, command=self.on_slider_change_real) # スライダー変更時イベント
        real_slider.pack() # スライダーを配置

        # 虚部のコントロール
        ttk.Label(self, text="虚部:").pack()
        vcmd = (self.register(self.validate_imag), '%P')
        imag_entry = ttk.Entry(self, textvariable=self.main_window.imag, width=20, validate='key', validatecommand=vcmd)
        imag_entry.pack()
        imag_entry.bind('<Return>', self.on_entry_change)
        imag_entry.bind('<FocusOut>', self.on_entry_change)
        imag_slider = ttk.Scale(self, from_=-2.0, to=2.0, variable=self.main_window.imag,
                                    orient=tk.HORIZONTAL, command=self.on_slider_change_imag)
        imag_slider.pack()

        # 反復回数のコントロール
        ttk.Label(self, text="反復回数:").pack()
        vcmd = (self.register(self.validate_max_iter), '%P')
        iter_entry = ttk.Entry(self, textvariable=self.main_window.max_iter, width=10, validate='key', validatecommand=vcmd)
        iter_entry.pack()
        iter_entry.bind('<Return>', self.on_iter_change)
        iter_entry.bind('<FocusOut>', self.on_iter_change)

        # 開始色のカラーマップのコントロール
        ttk.Label(self, text="開始色:").pack()
        color_frame1 = ttk.Frame(self) # フレームを作成
        color_frame1.pack(fill=tk.X, pady=2) # フレームを配置

        # 開始色のコントロール
        vcmd = (self.register(self.validate_start_color), '%P')
        start_color_entry = ttk.Entry(color_frame1, textvariable=self.main_window.start_color, width=8, validate='key', validatecommand=vcmd)
        start_color_entry.pack(side=tk.LEFT, padx=2)
        start_color_entry.bind('<Return>', self.on_color_change_start)
        start_color_entry.bind('<FocusOut>', self.on_color_change_start)

        # カラーパレットを表示するボタン
        ttk.Button(color_frame1, text="選択",
                         command=lambda: self.choose_color('start')).pack(side=tk.LEFT)

        # 終了色のカラーマップのコントロール
        ttk.Label(self, text="終了色:").pack()
        color_frame2 = ttk.Frame(self)
        color_frame2.pack(fill=tk.X, pady=2)

        # 終了色のコントロール
        vcmd = (self.register(self.validate_end_color), '%P')
        end_color_entry = ttk.Entry(color_frame2, textvariable=self.main_window.end_color, width=8, validate='key', validatecommand=vcmd)
        end_color_entry.pack(side=tk.LEFT, padx=2)
        end_color_entry.bind('<Return>', self.on_color_change_end)
        end_color_entry.bind('<FocusOut>', self.on_color_change_end)

        # カラーパレットを表示するボタン
        ttk.Button(color_frame2, text="選択",
                         command=lambda: self.choose_color('end')).pack(side=tk.LEFT)

        # 更新ボタン
        ttk.Button(self, text="更新", command=self.full_draw).pack(pady=10)

        # リセットボタンの追加
        ttk.Button(self, text="リセット", command=self.reset_params).pack(pady=10)

    # --- バリデーション関数(入力フォームの値が更新されたときに呼び出される) ---
    def validate_real(self, value):
        """実数部のバリデーション"""
        try:
            value = float(value)  # 実数に変換可能か確認
            return True
        except ValueError:
            return False  # 変換できなければ無効

    def validate_imag(self, value):
        """虚数部のバリデーション"""
        try:
            value = float(value)  # 実数に変換可能か確認
            return True
        except ValueError:
            return False  # 変換できなければ無効

    def validate_max_iter(self, value):
        """最大反復回数のバリデーション"""
        try:
            value = int(value)  # 整数に変換可能か確認
            if value > 0:  # 0より大きければ有効
                return True
            else:
                return False
        except ValueError:
            return False  # 変換できなければ無効

    def validate_start_color(self, color_hex):
        """開始色のバリデーション"""
        return color_map.is_valid_hex_color(color_hex)  # 16進数カラーコードの検証

    def validate_end_color(self, color_hex):
        """終了色のバリデーション"""
        return color_map.is_valid_hex_color(color_hex)  # 16進数カラーコードの検証

    # --- イベントハンドラ (コントロールパネル) ---
    def on_slider_change_real(self, value):
        try: # 例外処理
            real_val = float(value) # スライダーの値を数値に変換
            self.main_window.set_real_param(real_val) # MainWindowのパラメータ設定関数を呼び出す
        except ValueError: # 例外処理
            pass # スライダーの値が数値に変換できない場合は何もしない

    # --- スライダーの値を更新 ---
    def on_slider_change_imag(self, value):
        try:
            imag_val = float(value)
            self.main_window.set_imag_param(imag_val)
        except ValueError:
            pass

    # --- エントリーの値を更新 ---
    def on_entry_change(self, event):
        try:
            # 入力値を検証
            real_val = float(self.main_window.real.get()) # MainWindowの変数を参照
            imag_val = float(self.main_window.imag.get())
            # 値の範囲を制限
            self.main_window.set_real_param(max(-2.0, min(2.0, real_val))) # MainWindowのパラメータ設定関数を呼び出す
            self.main_window.set_imag_param(max(-2.0, min(2.0, imag_val)))
        except ValueError:
            # 無効な入力の場合は以前の値に戻す (エントリーの値は StringVar で管理しているので、ここでは何もしない)
            pass

    # --- 反復回数のエントリーの値を更新 ---
    def on_iter_change(self, event):
        try:
            # 入力値を検証
            iter_val = int(self.main_window.max_iter.get()) # MainWindowの変数を参照
            # 最小値を1に制限
            self.main_window.set_max_iter_param(max(1, iter_val)) # MainWindowのパラメータ設定関数を呼び出す
        except ValueError:
            # 無効な入力の場合は以前の値に戻す (エントリーの値は StringVar で管理しているので、ここでは何もしない)
            pass

    # --- カラーパレットを表示して開始色を選択 ---
    def on_color_change_start(self, event):
        start_color = self.main_window.start_color.get() # MainWindowの変数を参照
        if not color_map.is_valid_hex_color(start_color): # color_mapモジュールの関数を使用
            self.main_window.set_start_color_param("#0000FF") # デフォルトの開始色

    # --- カラーパレットを表示して終了色を選択 ---
    def on_color_change_end(self, event):
        end_color = self.main_window.end_color.get()
        if not color_map.is_valid_hex_color(end_color):
            self.main_window.set_end_color_param("#FFFFFF")

    # --- カラーパレットを表示して色を選択 ---
    def choose_color(self, color_type):
        current_color = self.main_window.start_color.get() if color_type == 'start' else self.main_window.end_color.get() # MainWindowの変数を参照
        title = f"{color_type.capitalize()}色の選択" # ウィンドウのタイトルを設定
        selected_color = color_map.choose_color(self, current_color, title) # color_mapモジュールの関数を使用
        if selected_color: # 色が選択された場合
            if color_type == 'start': # 開始色の場合
                self.main_window.set_start_color_param(selected_color) # MainWindowのパラメータ設定関数を呼び出す
            else: # 終了色の場合
                self.main_window.set_end_color_param(selected_color) # MainWindowのパラメータ設定関数を呼び出す

    # --- 描画を更新 ---
    def full_draw(self):
        self.main_window.full_draw() # MainWindowの描画関数を呼び出す

    # --- パラメータをリセット ---
    def reset_params(self):
        self.main_window.reset_params() # MainWindowのリセット関数を呼び出す
