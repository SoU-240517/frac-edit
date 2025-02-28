import tkinter as tk
import numpy as np
from tkinter import ttk
from PIL import Image, ImageTk
from .control_panel import ControlPanel
from core import fractal, color_map

class MainWindow: # --- MainWindowのクラス定義 ---
    def __init__(self, root): # --- MainWindowクラスのコンストラクタの定義 ---
        self.root = root # 渡されたrootを、このオブジェクトのroot属性として保存する
        self.root.title("Julia Set Viewer") # ウィンドウのタイトルを設定
        # メインフレームの設定
        self.main_frame = ttk.Frame(root) # ttk.Frameクラスを使用してメインフレームを作成
        self.main_frame.pack(fill=tk.BOTH, expand=True) # メインフレームをウィンドウ全体に広げて配置
        # キャンバスの設定
        self.canvas_width = 1280 # キャンバスの幅を1280ピクセルに設定
        self.canvas_height = 720 # キャンバスの高さを720ピクセルに設定
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height, bg='white') # Canvasクラスを使用してキャンバスを作成（背景色は白）
        self.canvas.pack(side=tk.LEFT) # キャンバスをメインフレームの左側に配置

        # パラメータの初期値をここで一元管理
        self.initial_params = {
            'real': -0.4,
            'imag': 0.6,
            'max_iter': 300,
            'start_color': "#0000FF",
            'end_color': "#FFFFFF",
            'bg_color': "#000000"
        }

        # 実際に使用するパラメータ
        self.real = tk.DoubleVar(value=self.initial_params['real'])
        self.imag = tk.DoubleVar(value=self.initial_params['imag'])
        self.max_iter = tk.IntVar(value=self.initial_params['max_iter'])
        self.start_color = tk.StringVar(value=self.initial_params['start_color'])
        self.end_color = tk.StringVar(value=self.initial_params['end_color'])
        self.bg_color = tk.StringVar(value=self.initial_params['bg_color'])

        # ビュー範囲の初期値
        self.view_x_min = -2.0 # ビューのX軸最小値を-2.0に設定
        self.view_x_max = 2.0 # ビューのX軸最大値を2.0に設定
        self.view_y_min = -2.0 # ビューのY軸最小値を-2.0に設定
        self.view_y_max = 2.0 # ビューのY軸最大値を2.0に設定
        # 初期値を辞書型（キーと値のペアでデータを管理する形式）で保存
        self.initial_view = {
            'x_min': -2.0, # 初期のX軸最小値
            'x_max': 2.0, # 初期のX軸最大値
            'y_min': -2.0, # 初期のY軸最小値
            'y_max': 2.0 # 初期のY軸最大値
        }
        # マウスイベントのバインド（検知）と対応する関数の呼び出し設定
        self.canvas.bind('<MouseWheel>', self.on_mousewheel) # マウスホイールを検知したらon_mousewheel関数を呼び出す
        self.canvas.bind('<Button-4>', self.on_mousewheel) # マウスホイール上回転を検知したらon_mousewheel関数を呼び出す（Linux用）
        self.canvas.bind('<Button-5>', self.on_mousewheel) # マウスホイール下回転を検知したらon_mousewheel関数を呼び出す（Linux用）
        self.canvas.bind('<Button-3>', self.start_pan) # 右クリックを検知したらstart_pan関数を呼び出す
        self.canvas.bind('<B3-Motion>', self.on_pan) # 右ドラッグを検知したらon_pan関数を呼び出す
        # パンの初期化
        self.pan_start_x = None # パン操作の開始X座標を初期化
        self.pan_start_y = None # パン操作の開始Y座標を初期化
        # コントロールパネルの設定 (ControlPanelクラスを使用)
        self.control_panel = ControlPanel(self.main_frame, self) # MainWindowを親としてControlPanelを作成
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y) # コントロールパネルをメインフレームの右側に配置
        # 初回描画
        self.quick_draw() # 初期状態で簡易描画を実行

    def quick_draw(self): # --- 簡易描画の場合の処理 ---
        self._draw(quick=True)

    def full_draw(self): # --- 完全描画の場合の処理 ---
        self._draw(quick=False)

    def _draw(self, quick=False): # --- 描画処理の共通部分 ---
        if quick: # 簡易描画の場合は間引く
            skip = 4
        else: # 完全描画の場合は間引かない
            skip = 1
        # calculate_juliaに引数を渡して、結果をoutputに格納する
        output = fractal.calculate_julia(
            self.view_x_min, self.view_x_max,
            self.view_y_min, self.view_y_max,
            self.canvas_width, self.canvas_height,
            self.real.get(), self.imag.get(), # 実部と虚部の値を入力フィールドから取得
            self.max_iter.get(), skip # 最大反復回数と間引き回数を入力フィールドから取得
        )
        # カラーマップの適用 (color_mapモジュールの関数を使用)
        colors = color_map.create_colormap(
            output,
            self.start_color.get(), # 開始色の値を入力フィールドから取得
            self.end_color.get(), # 終了色の値を入力フィールドから取得
            self.bg_color.get() # 背景色の値を入力フィールドから取得
        )
        # 画像の拡大 (簡易描画時のみ)
        if quick: # 簡易描画の場合
            if len(colors.shape) != 3:
                raise ValueError(f"Invalid colors shape: {colors.shape}, expected (height, width, 3)")
            colors_resized = np.repeat(np.repeat(colors, skip, axis=0), skip, axis=1) # 1ピクセルを縦横skip倍のブロックに拡大（np.repeatはNumPyの関数で、配列の要素を指定した回数だけ繰り返す）
            img = Image.fromarray(colors_resized) # PIL（Python Imaging Library）のImage.fromarrayで画像オブジェクトに変換
        else: # 完全描画の場合はそのまま
            img = Image.fromarray(colors) # PIL（Python Imaging Library）のImage.fromarrayで画像オブジェクトに変換
        self.photo = ImageTk.PhotoImage(image=img) # imgをTkinterで使える形式（PhotoImage形式）に変換
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW) # 画像をキャンバスに描画（0, 0は原点で、画像の左上の座標。tk.NWは「North West（北西）」つまり左上に配置する

    def on_mousewheel(self, event): # --- イベントハンドラ（マウス操作） ---
        # マウスの座標を取得
        canvas_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        canvas_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        # マウスの座標を複素数に変換
        complex_x = self.view_x_min + (self.view_x_max - self.view_x_min) * (canvas_x / self.canvas_width)
        complex_y = self.view_y_min + (self.view_y_max - self.view_y_min) * (canvas_y / self.canvas_height)
        # ズームイン/アウトの処理
        if event.num == 4 or event.delta > 0: # ホイール上回転
            zoom_factor = 0.9 # ズームイン
        else: # ホイール下回転
            zoom_factor = 1.1 # ズームアウト
        # 倍率に応じてビュー範囲を更新
        width = (self.view_x_max - self.view_x_min) * zoom_factor # 幅の計算
        height = (self.view_y_max - self.view_y_min) * zoom_factor # 高さの計算
        # マウス位置を新しい中心にして表示範囲をずらす
        self.view_x_min = complex_x - width * (canvas_x / self.canvas_width)
        self.view_x_max = complex_x + width * (1 - canvas_x / self.canvas_width)
        self.view_y_min = complex_y - height * (canvas_y / self.canvas_height)
        self.view_y_max = complex_y + height * (1 - canvas_y / self.canvas_height)
        # 簡易描画
        self.quick_draw()

    def start_pan(self, event): # --- イベントハンドラ（パン） ---
        # パンの開始位置を記録
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def on_pan(self, event): # --- キャンバスをドラッグして表示範囲を移動するためのイベントハンドラ ---
        if self.pan_start_x is None or self.pan_start_y is None: # パンの開始位置が未設定なら何もしない
            return
        # ドラッグ距離を計算（現在のマウス位置とパンの開始位置の差）
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        # スケールを計算（キャンバスのピクセル数に対するビュー範囲の比率）
        x_scale = (self.view_x_max - self.view_x_min) / self.canvas_width
        y_scale = (self.view_y_max - self.view_y_min) / self.canvas_height
        # ドラッグ距離をビュー範囲のスケールに変換（移動量を複素平面に適用）
        dx_complex = -dx * x_scale
        dy_complex = -dy * y_scale
        # ビュー範囲を更新（ドラッグに応じて全体を移動）
        self.view_x_min += dx_complex
        self.view_x_max += dx_complex
        self.view_y_min += dy_complex
        self.view_y_max += dy_complex
        # パンの開始位置を現在のマウス位置に更新
        self.pan_start_x = event.x # パンの開始位置 (x座標)
        self.pan_start_y = event.y # パンの開始位置 (y座標)
        # 簡易描画
        self.quick_draw()

    def reset_view(self): # --- ビュー範囲を初期状態に戻す（ControlPanelに移動しても良い） ---
        self.view_x_min = self.initial_view['x_min']
        self.view_x_max = self.initial_view['x_max']
        self.view_y_min = self.initial_view['y_min']
        self.view_y_max = self.initial_view['y_max']
        # 簡易描画
        self.quick_draw()

    def reset_params(self): # --- パラメータを初期値に戻す（ビューもリセット）（ControlPanelに移動しても良い） ---
        self.real.set(self.initial_params['real'])
        self.imag.set(self.initial_params['imag'])
        self.max_iter.set(self.initial_params['max_iter'])
        self.start_color.set(self.initial_params['start_color'])
        self.end_color.set(self.initial_params['end_color'])
        self.bg_color.set(self.initial_params['bg_color'])
        self.reset_view() # ビュー範囲を初期状態に戻す

    def set_real_param(self, value): # --- 実部の値をControlPanelから設定するメソッド ---
        self.real.set(value) # パラメータを設定
        self.quick_draw() # 簡易描画

    def set_imag_param(self, value): # --- 虚部の値をControlPanelから設定するメソッド ---
        self.imag.set(value) # パラメータを設定
        self.quick_draw() # 簡易描画

    def set_max_iter_param(self, value): # --- 最大反復回数の値をControlPanelから設定するメソッド ---
        self.max_iter.set(value) # パラメータを設定
        self.quick_draw() # 簡易描画

    def set_start_color_param(self, color_hex): # --- 開始色の値をControlPanelから設定するメソッド ---
        try: # 入力されたカラーコードを処理
            if color_map.is_valid_hex_color(color_hex): # カラーコードが有効な16進数なら
                self.start_color.set(color_hex) # 入力された値を開始色に設定
            else: # カラーコードが無効な場合
                self.start_color.set(self.initial_params['start_color']) # デフォルトの青を設定
        except: # 例外が発生した場合（例: フォーマットエラー）
            self.start_color.set(self.initial_params['start_color']) # デフォルトの青を設定
        finally: # 処理の成否に関わらず
            self.quick_draw() # 簡易描画

    def set_end_color_param(self, color_hex): # --- 終了色の値をControlPanelから設定するメソッド ---
        try:
            if color_map.is_valid_hex_color(color_hex):
                self.end_color.set(color_hex)
            else:
                self.end_color.set("#0000FF")
        except :
            self.end_color.set(self.initial_params['end_color'])
        finally:
            self.quick_draw()

    def set_bg_color_param(self, color_hex): # --- 背景色の値をControlPanelから設定するメソッド ---
        try:
            if color_map.is_valid_hex_color(color_hex): # カラーコードが有効な16進数なら
                self.bg_color.set(color_hex)
                self.canvas.configure(bg=color_hex) # キャンバスの背景色を更新
            else:
                self.bg_color.set(self.initial_params['bg_color'])
                self.canvas.configure(bg=self.initial_params['bg_color'])
        except:
            self.bg_color.set(self.initial_params['bg_color'])
            self.canvas.configure(bg=self.initial_params['bg_color'])
        finally:
            self.quick_draw()
