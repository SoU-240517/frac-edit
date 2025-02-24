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
        vcmd = (self.register(self.validate_start_color), '%P') # 入力値を検証する関数を登録
        start_color_entry = ttk.Entry(color_frame1, textvariable=self.main_window.start_color, width=8, validate='key', validatecommand=vcmd) # MainWindowの変数を参照
        start_color_entry.pack(side=tk.LEFT, padx=2) # エントリーを配置
        start_color_entry.bind('<Return>', lambda e: self.on_color_change_start(e, force=True)) # Enterキーで変更
        start_color_entry.bind('<FocusOut>', lambda e: self.on_color_change_start(e, force=True)) # フォーカスを失ったときに変更

        # カラーパレットを表示するボタン
        ttk.Button(color_frame1, text="選択", command=lambda: self.choose_color('start')).pack(side=tk.LEFT)

        # 終了色のカラーマップのコントロール
        ttk.Label(self, text="終了色:").pack()
        color_frame2 = ttk.Frame(self)
        color_frame2.pack(fill=tk.X, pady=2)

        # 終了色のコントロール
        vcmd = (self.register(self.validate_end_color), '%P')
        end_color_entry = ttk.Entry(color_frame2, textvariable=self.main_window.end_color, width=8, validate='key', validatecommand=vcmd)
        end_color_entry.pack(side=tk.LEFT, padx=2)
        end_color_entry.bind('<Return>', lambda e: self.on_color_change_end(e, force=True))
        end_color_entry.bind('<FocusOut>', lambda e: self.on_color_change_end(e, force=True))

        # カラーパレットを表示するボタン
        ttk.Button(color_frame2, text="選択", command=lambda: self.choose_color('end')).pack(side=tk.LEFT)

        # 更新ボタン
        ttk.Button(self, text="更新", command=self.full_draw).pack(pady=10)

        # リセットボタンの追加
        ttk.Button(self, text="リセット", command=self.reset_params).pack(pady=10)

    # 実部の入力値の検証
    def validate_real(self, value):
        try:
            value = float(value) # 実数に変換可能か確認
            return True # 変換できれば有効
        except ValueError:
            return False # 変換できなければ無効

    # 虚部の入力値の検証
    def validate_imag(self, value):
        try:
            value = float(value)
            return True
        except ValueError:
            return False

    # 反復回数の入力値の検証
    def validate_max_iter(self, value):
        try:
            value = int(value) # 整数に変換可能か確認
            if value > 0: # 0より大きければ有効
                return True # 変換できれば有効
            else:
                return False # 変換できなければ無効
        except ValueError:
            return False  # 変換できなければ無効

    # 開始色の入力値の検証
    def validate_start_color(self, color_hex):
        if not color_hex: return True # 空文字列は有効
        if color_hex == "#": return True # 空文字列は有効
        if len(color_hex) > 7: return False # 7文字以上は無効
        return color_hex.startswith('#') and all(c in '0123456789abcdefABCDEF' for c in color_hex[1:]) # 16進数の形式か確認

    # 終了色の入力値の検証
    def validate_end_color(self, color_hex):
        if not color_hex: return True
        if color_hex == "#": return True
        if len(color_hex) > 7: return False
        return color_hex.startswith('#') and all(c in '0123456789abcdefABCDEF' for c in color_hex[1:])

    # 実部のスライダーの値を更新
    def on_slider_change_real(self, value):
        try:
            real_val = float(value) # スライダーの値を数値に変換
            self.main_window.set_real_param(real_val) # MainWindowのパラメータ設定関数を呼び出す
        except ValueError:
            pass # スライダーの値が数値に変換できない場合は何もしない

    # 虚部のスライダーの値を更新
    def on_slider_change_imag(self, value):
        try:
            imag_val = float(value)
            self.main_window.set_imag_param(imag_val)
        except ValueError:
            pass

    # 実部と虚部の変更値を反映
    def on_entry_change(self, event):
        try:
            real_val = float(self.main_window.real.get()) # 変更された実部の値を取得
            imag_val = float(self.main_window.imag.get()) # 変更された虚部の値を取得
            self.main_window.set_real_param(max(-2.0, min(2.0, real_val))) # real_valの値が-2.0より小さい場合、-2.0をがset_real_paramメソッドに渡す
            self.main_window.set_imag_param(max(-2.0, min(2.0, imag_val))) # imag_valの値が-2.0より小さい場合、-2.0をがset_imag_paramメソッドに渡す
        except ValueError:
            pass # 無効な入力の場合は以前の値に戻す (エントリーの値は StringVar で管理しているので、ここでは何もしない)

    # 反復回数の変更値を反映
    def on_iter_change(self, event):
        try:
            iter_val = int(self.main_window.max_iter.get()) # 変更された反復回数の値を取得
            self.main_window.set_max_iter_param(max(1, iter_val)) # iter_valの値が1より小さい場合、1をがset_max_iter_paramメソッドに渡す
        except ValueError:
            # 無効な入力の場合は以前の値に戻す (エントリーの値は StringVar で管理しているので、ここでは何もしない)
            pass

    # --- カラーパレットを表示して開始色を選択 ---
    def on_color_change_start(self, event, force=False):
        start_color = self.main_window.start_color.get() # 現在の開始色を取得
        if force or not color_map.is_valid_hex_color(start_color): # 無効なカラーコードであるか、またはforce引数がTrueである場合
            self.main_window.set_start_color_param(start_color) # 取得した色の値をメインウィンドウの開始色パラメータとして設定

    # --- カラーパレットを表示して終了色を選択 ---
    def on_color_change_end(self, event, force=False):
        end_color = self.main_window.end_color.get()
        if force or not color_map.is_valid_hex_color(end_color):
            self.main_window.set_end_color_param(end_color)

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
