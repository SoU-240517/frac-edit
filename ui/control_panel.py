import tkinter as tk
from tkinter import ttk
from core import color_map

class ControlPanel(ttk.Frame): # --- ControlPanelクラスの定義 ---
    def __init__(self, parent, main_window): # --- ControlPanelクラスのコンストラクタの定義 ---
        super().__init__(parent, padding="10") # 親クラスの初期化を実行（パディング10を設定）
        self.main_window = main_window # MainWindowへの参照を保存
        self.setup_panel() # コントロールパネルのUIを構築

    def setup_panel(self): # --- コントロールパネルのUIを構築するメソッド ---
        # 実部の入力欄を作成
        ttk.Label(self, text="実部:").pack()
        vcmd = (self.register(self.validate_real), '%P') # 実部の入力値を検証するコールバックを登録
        real_entry = ttk.Entry(self, textvariable=self.main_window.real, width=20, validate='key', validatecommand=vcmd) # 実部用の入力欄を設定（MainWindowの変数と連動）
        real_entry.pack() # 入力欄を配置
        real_entry.bind('<Return>', self.on_entry_change) # Enterキーを押したときに値を更新
        real_entry.bind('<FocusOut>', self.on_entry_change) # 入力欄からフォーカスが外れたときに値を更新
        # 実部用のスライダーを設定（範囲-2.0～2.0、MainWindowの変数と連動）し、スライダー操作時に実部を更新
        real_slider = ttk.Scale(self, from_=-2.0, to=2.0, variable=self.main_window.real,
                                    orient=tk.HORIZONTAL, command=self.on_slider_change_real)
        real_slider.pack() # スライダーを配置

        # 虚部の入力欄を作成
        ttk.Label(self, text="虚部:").pack()
        vcmd = (self.register(self.validate_imag), '%P')
        imag_entry = ttk.Entry(self, textvariable=self.main_window.imag, width=20, validate='key', validatecommand=vcmd)
        imag_entry.pack()
        imag_entry.bind('<Return>', self.on_entry_change)
        imag_entry.bind('<FocusOut>', self.on_entry_change)
        imag_slider = ttk.Scale(self, from_=-2.0, to=2.0, variable=self.main_window.imag,
                                    orient=tk.HORIZONTAL, command=self.on_slider_change_imag)
        imag_slider.pack()

        # 反復回数の入力欄を作成
        ttk.Label(self, text="反復回数:").pack()
        vcmd = (self.register(self.validate_max_iter), '%P')
        iter_entry = ttk.Entry(self, textvariable=self.main_window.max_iter, width=10, validate='key', validatecommand=vcmd)
        iter_entry.pack()
        iter_entry.bind('<Return>', self.on_iter_change)
        iter_entry.bind('<FocusOut>', self.on_iter_change)

        # 開始色の入力欄を作成
        ttk.Label(self, text="開始色:").pack()
        start_color_frame = ttk.Frame(self) # 開始色用のフレームを作成
        start_color_frame.pack(fill=tk.X, pady=2) # フレームを横に広げて配置（上下に余白2）
        vcmd = (self.register(self.validate_start_color), '%P') # 開始色の入力値を検証するコールバックを登録
        start_color_entry = ttk.Entry(start_color_frame, textvariable=self.main_window.start_color, width=8, validate='key', validatecommand=vcmd) # 開始色用の入力欄を設定（メインウィンドウの変数と連動）
        start_color_entry.pack(side=tk.LEFT, padx=2) # 入力欄を左寄せで配置（左右に余白2）
        start_color_entry.bind('<Return>', lambda e: self.on_color_change_start(e, force=True)) # Enterキーを押したときに値を更新
        start_color_entry.bind('<FocusOut>', lambda e: self.on_color_change_start(e, force=True)) # 入力欄からフォーカスが外れたときに値を更新
        ttk.Button(start_color_frame, text="選択", command=lambda: self.choose_color('start')).pack(side=tk.LEFT) # カラーピッカーを開くボタンを左寄せで配置

        # 終了色の入力欄を作成
        ttk.Label(self, text="終了色:").pack()
        end_color_frame = ttk.Frame(self)
        end_color_frame.pack(fill=tk.X, pady=2)
        vcmd = (self.register(self.validate_end_color), '%P')
        end_color_entry = ttk.Entry(end_color_frame, textvariable=self.main_window.end_color, width=8, validate='key', validatecommand=vcmd)
        end_color_entry.pack(side=tk.LEFT, padx=2)
        end_color_entry.bind('<Return>', lambda e: self.on_color_change_end(e, force=True))
        end_color_entry.bind('<FocusOut>', lambda e: self.on_color_change_end(e, force=True))
        ttk.Button(end_color_frame, text="選択", command=lambda: self.choose_color('end')).pack(side=tk.LEFT)

        # 背景色の入力欄を作成
        ttk.Label(self, text="背景色:").pack()
        bg_color_frame = ttk.Frame(self)
        bg_color_frame.pack(fill=tk.X, pady=2)
        vcmd = (self.register(self.validate_bg_color), '%P')
        bg_color_entry = ttk.Entry(bg_color_frame, textvariable=self.main_window.bg_color, width=8, validate='key', validatecommand=vcmd)
        bg_color_entry.pack(side=tk.LEFT, padx=2)
        bg_color_entry.bind('<Return>', lambda e: self.on_color_change_bg(e, force=True))
        bg_color_entry.bind('<FocusOut>', lambda e: self.on_color_change_bg(e, force=True))
        ttk.Button(bg_color_frame, text="選択", command=lambda: self.choose_color('bg')).pack(side=tk.LEFT)

        # 更新ボタン
        ttk.Button(self, text="更新", command=self.full_draw).pack(pady=10)

        # リセットボタンの追加
        ttk.Button(self, text="リセット", command=self.reset_params).pack(pady=10)

    def validate_real(self, value): # --- 実部の入力値の検証するメソッド ---
        try:
            value = float(value) # 実数に変換可能か確認
            return True # 変換できれば有効
        except ValueError:
            return False # 変換できなければ無効

    def validate_imag(self, value): # --- 虚部の入力値の検証するメソッド ---
        try:
            value = float(value)
            return True
        except ValueError:
            return False

    def validate_max_iter(self, value): # --- 反復回数の入力値の検証するメソッド ---
        try:
            value = int(value) # 整数に変換可能か確認
            if value > 0: # 0より大きければ有効
                return True # 変換できれば有効
            else:
                return False # 変換できなければ無効
        except ValueError:
            return False  # 変換できなければ無効

    def validate_start_color(self, color_hex): # --- 開始色の入力値を16進数形式で検証するメソッド ---
        if not color_hex: return True # 空文字列は許可（未入力として有効）
        if color_hex == "#": return True # "#"のみも許可（入力開始として有効）
        if len(color_hex) > 7: return False # 7文字を超える場合は無効（#RRGGBB形式を超えるため）
        return color_hex.startswith('#') and all(c in '0123456789abcdefABCDEF' for c in color_hex[1:]) # "#"で始まり、以降が16進数文字なら有効

    def validate_end_color(self, color_hex): # --- 終了色の入力値を16進数形式で検証するメソッド ---
        if not color_hex: return True
        if color_hex == "#": return True
        if len(color_hex) > 7: return False
        return color_hex.startswith('#') and all(c in '0123456789abcdefABCDEF' for c in color_hex[1:])

    def validate_bg_color(self, color_hex): # --- 背景色の入力値を16進数形式で検証するメソッド ---
        if not color_hex: return True
        if color_hex == "#": return True
        if len(color_hex) > 7: return False
        return color_hex.startswith('#') and all(c in '0123456789abcdefABCDEF' for c in color_hex[1:])

    def on_slider_change_real(self, value): # --- 実部のスライダーが動かされたときに呼ばれるメソッド ---
        try:
            real_val = float(value) # スライダーの値を浮動小数点数に変換
            self.main_window.set_real_param(real_val) # MainWindowの実部パラメータを更新
        except ValueError: # 値が数値に変換できない場合
            pass # 例外を無視して処理をスキップ

    def on_slider_change_imag(self, value): # --- 虚部のスライダーが動かされたときに呼ばれるメソッド ---
        try:
            imag_val = float(value)
            self.main_window.set_imag_param(imag_val)
        except ValueError:
            pass

    def on_entry_change(self, event): # --- 実部と虚部の入力欄の値が変更されたときに呼ばれるメソッド ---
        try:
            real_val = float(self.main_window.real.get()) # 変更された実部の値を取得
            imag_val = float(self.main_window.imag.get()) # 変更された虚部の値を取得
            self.main_window.set_real_param(max(-2.0, min(2.0, real_val))) # real_valの値が-2.0より小さい場合、-2.0をがset_real_paramメソッドに渡す
            self.main_window.set_imag_param(max(-2.0, min(2.0, imag_val))) # imag_valの値が-2.0より小さい場合、-2.0をがset_imag_paramメソッドに渡す
        except ValueError:
            pass # 無効な入力の場合は以前の値に戻す (エントリーの値は StringVar で管理しているので、ここでは何もしない)

    def on_iter_change(self, event): # --- 反復回数の入力欄の値が変更されたときに呼ばれるメソッド ---
        try:
            iter_val = int(self.main_window.max_iter.get()) # 変更された反復回数の値を取得
            self.main_window.set_max_iter_param(max(1, iter_val)) # iter_valの値が1より小さい場合、1をがset_max_iter_paramメソッドに渡す
        except ValueError:
            # 無効な入力の場合は以前の値に戻す (エントリーの値は StringVar で管理しているので、ここでは何もしない)
            pass

    def on_color_change_start(self, event, force=False): # --- カラーパレットを表示して開始色を選択 ---
        start_color = self.main_window.start_color.get() # 現在の開始色を取得
        if force or not color_map.is_valid_hex_color(start_color): # 無効なカラーコードであるか、またはforce引数がTrueである場合
            self.main_window.set_start_color_param(start_color) # 取得した色の値をメインウィンドウの開始色パラメータとして設定

    def on_color_change_end(self, event, force=False): # --- カラーパレットを表示して終了色を選択 ---
        end_color = self.main_window.end_color.get()
        if force or not color_map.is_valid_hex_color(end_color):
            self.main_window.set_end_color_param(end_color)

    def on_color_change_bg(self, event, force=False): # --- カラーパレットを表示して背景色を選択 ---
        bg_color = self.main_window.bg_color.get()
        if force or not color_map.is_valid_hex_color(bg_color):
            self.main_window.set_bg_color_param(bg_color)

    def choose_color(self, color_type):  # --- カラーピッカーを開いて指定されたタイプの色を選択するメソッド ---
        # 現在の色を取得（color_type に応じて start, end, bg から選択）
        color_map_dict = {
            'start': self.main_window.start_color,
            'end': self.main_window.end_color,
            'bg': self.main_window.bg_color
        }
        current_color = color_map_dict[color_type].get()  # 対応する色の現在の値を取得
        title = f"{color_type.capitalize()}色の選択"  # カラーピッカーのウィンドウタイトルを設定（例: "Start色の選択"）
        selected_color = color_map.choose_color(self, current_color, title)  # color_mapモジュールを使って色を選択
        if selected_color:  # 色が選択された場合
            # 選択した色を対応するパラメータに設定
            param_setters = {
                'start': self.main_window.set_start_color_param,
                'end': self.main_window.set_end_color_param,
                'bg': self.main_window.set_bg_color_param
            }
            param_setters[color_type](selected_color)  # 該当する設定メソッドを呼び出して色を更新

    def full_draw(self): # --- 描画を更新 ---
        self.main_window.full_draw() # MainWindowの完全描画関数を呼び出す

    def reset_params(self): # --- パラメータをリセット ---
        self.main_window.reset_params() # MainWindowのリセット関数を呼び出す
