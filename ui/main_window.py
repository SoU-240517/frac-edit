import tkinter as tk # Tkinterのインポート
import numpy as np # NumPyのインポート
from tkinter import ttk # ttkのインポート
from PIL import Image, ImageTk # PILのインポート
from .control_panel import ControlPanel # ControlPanelクラスのインポート
from core import fractal, color_map # coreモジュールのインポート

# --- メインウィンドウのクラス定義 ---
class MainWindow:
    # --- コンストラクタ ---
    def __init__(self, root):
        self.root = root # Tkクラスのインスタンスを保存
        self.root.title("Julia Set Viewer") # ウィンドウタイトルの設定

        # パラメータの初期値 (ControlPanelに移動しても良い)
        self.real = tk.DoubleVar(value=-0.4) # DoubleVarクラスを使用
        self.imag = tk.DoubleVar(value=0.6)
        self.max_iter = tk.IntVar(value=100) # IntVarクラスを使用
        self.start_color = tk.StringVar(value="#0000FF") # 青
        self.end_color = tk.StringVar(value="#FFFFFF") # 白

        # ビュー範囲の初期値
        self.view_x_min = -2.0
        self.view_x_max = 2.0
        self.view_y_min = -2.0
        self.view_y_max = 2.0

        # 初期値を辞書型で保存
        self.initial_view = {
            'x_min': -2.0,
            'x_max': 2.0,
            'y_min': -2.0,
            'y_max': 2.0
        }

        # メインフレームの設定
        self.main_frame = ttk.Frame(root) # ttk.Frameクラスを使用
        self.main_frame.pack(fill=tk.BOTH, expand=True) # メインフレームを配置

        # キャンバスの設定
        self.canvas_width = 800 # キャンバスの幅
        self.canvas_height = 500 # キャンバスの高さ
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height, bg='white') # Canvasクラスを使用
        self.canvas.pack(side=tk.LEFT) # キャンバスを配置

        # マウスイベントのバインド（検知）と対応する関数の呼び出し設定
        """
            '<Button-1>': マウスの左ボタンクリック
            '<Button-2>': マウスの中ボタンクリック（またはホイールクリック）
            '<Button-3>': マウスの右ボタンクリック
            '<Button-4>': マウスホイールの上回転（スクロールアップ）
            '<Button-5>': マウスホイールの下回転（スクロールダウン）
        """
        self.canvas.bind('<MouseWheel>', self.on_mousewheel) # マウスホイールを検知したらon_mousewheel関数を呼び出す
        self.canvas.bind('<Button-4>', self.on_mousewheel) # マウスホイール上回転を検知したらon_mousewheel関数を呼び出す
        self.canvas.bind('<Button-5>', self.on_mousewheel) # マウスホイール下回転を検知したらon_mousewheel関数を呼び出す
        self.canvas.bind('<Button-3>', self.start_pan) # 右クリックを検知したらstart_pan関数を呼び出す
        self.canvas.bind('<B3-Motion>', self.on_pan) # 右ドラッグを検知したらon_pan関数を呼び出す

        # パンの初期化
        self.pan_start_x = None
        self.pan_start_y = None

        # コントロールパネルの設定 (ControlPanelクラスを使用)
        self.control_panel = ControlPanel(self.main_frame, self) # MainWindowを親とselfとして渡す
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y) # コントロールパネルを配置

        # 初回描画
        self.quick_draw()

    # --- 簡易描画の場合の処理 ---
    def quick_draw(self): # 簡易描画
        self._draw(quick=True)

    # --- 完全描画の場合の処理 ---
    def full_draw(self):
        self._draw(quick=False) # _draw関数を呼び出す

    # --- 描画処理の共通部分 ---
    def _draw(self, quick=False):
        if quick: # 簡易描画の場合は間引く
            skip = 4
        else: # 完全描画の場合は間引かない
            skip = 1

        output = fractal.calculate_julia( # fractalモジュールの関数を使用
            self.view_x_min, self.view_x_max, # ビュー範囲
            self.view_y_min, self.view_y_max,
            self.canvas_width, self.canvas_height, # キャンバスのサイズ
            self.real.get(), self.imag.get(), # パラメータ
            self.max_iter.get(), skip # 最大反復回数と間引き
        )

        # カラーマップの適用 (color_mapモジュールの関数を使用)
        colors = color_map.create_colormap(
            output, # 出力画像
            self.start_color.get(), # 開始色
            self.end_color.get() # 終了色
        )

        # 画像の拡大 (簡易描画時のみ)
        if quick: # 簡易描画の場合は画像を拡大
            colors_resized = np.repeat(np.repeat(colors, skip, axis=0), skip, axis=1) # 画像を拡大
            img = Image.fromarray(colors_resized) # 画像をPIL形式に変換
        else: # 完全描画の場合はそのまま
            img = Image.fromarray(colors) # 画像をPIL形式に変換

        self.photo = ImageTk.PhotoImage(image=img) # 画像をPhotoImage形式に変換
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW) # 画像をキャンバスに描画

    # --- イベントハンドラ (マウス操作) ---
    def on_mousewheel(self, event):
        canvas_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx() # キャンバス上のマウスのx座標
        canvas_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty() # キャンバス上のマウスのy座標
        complex_x = self.view_x_min + (self.view_x_max - self.view_x_min) * (canvas_x / self.canvas_width) # キャンバス上のx座標を複素数に変換
        complex_y = self.view_y_min + (self.view_y_max - self.view_y_min) * (canvas_y / self.canvas_height) # キャンバス上のy座標を複素数に変換

        if event.num == 4 or event.delta > 0: # マウスホイール上回転の場合
            zoom_factor = 0.9 # ズームイン
        else: # マウスホイール下回転の場合
            zoom_factor = 1.1 # ズームアウト

        width = (self.view_x_max - self.view_x_min) * zoom_factor # 幅の計算
        height = (self.view_y_max - self.view_y_min) * zoom_factor # 高さの計算

        # マウス位置を中心にズームイン/アウト
        self.view_x_min = complex_x - width * (canvas_x / self.canvas_width)
        self.view_x_max = complex_x + width * (1 - canvas_x / self.canvas_width)
        self.view_y_min = complex_y - height * (canvas_y / self.canvas_height)
        self.view_y_max = complex_y + height * (1 - canvas_y / self.canvas_height)

        self.quick_draw() # 簡易描画

    # --- イベントハンドラ (パン) ---
    def start_pan(self, event):
        self.pan_start_x = event.x # パンの開始位置 (x座標)
        self.pan_start_y = event.y # パンの開始位置 (y座標)

    # --- イベントハンドラ (パン中) ---
    def on_pan(self, event):
        if self.pan_start_x is None or self.pan_start_y is None: # パンの開始位置が未設定の場合は何もしない
            return

        dx = event.x - self.pan_start_x # ドラッグしたx方向の距離
        dy = event.y - self.pan_start_y # ドラッグしたy方向の距離

        x_scale = (self.view_x_max - self.view_x_min) / self.canvas_width # x方向のスケール
        y_scale = (self.view_y_max - self.view_y_min) / self.canvas_height # y方向のスケール

        dx_complex = -dx * x_scale # x方向の複素数
        dy_complex = -dy * y_scale # y方向の複素数

        # パンの処理
        self.view_x_min += dx_complex
        self.view_x_max += dx_complex
        self.view_y_min += dy_complex
        self.view_y_max += dy_complex

        self.pan_start_x = event.x # パンの開始位置 (x座標)
        self.pan_start_y = event.y # パンの開始位置 (y座標)

        self.quick_draw() # 簡易描画

    # --- パビュー範囲を初期状態に戻す ---
    def reset_view(self): # ControlPanelに移動しても良い
        self.view_x_min = self.initial_view['x_min']
        self.view_x_max = self.initial_view['x_max']
        self.view_y_min = self.initial_view['y_min']
        self.view_y_max = self.initial_view['y_max']
        self.quick_draw()

    # --- パラメータを初期値に戻す (ビューもリセット) ---
    def reset_params(self): # ControlPanelに移動しても良い
        """パラメータを初期値に戻す (ビューもリセット)"""
        self.real.set(-0.4)
        self.imag.set(0.6)
        self.max_iter.set(100)
        self.start_color.set("#0000FF")
        self.end_color.set("#FFFFFF")
        self.reset_view() # ビュー範囲を初期状態に戻す

    # --- パラメータ設定用関数（実数部） (ControlPanelから呼び出す) ---
    def set_real_param(self, value):
        self.real.set(value) # パラメータを設定
        self.quick_draw() # 簡易描画

    # --- パラメータ設定用関数（虚数部） (ControlPanelから呼び出す) ---
    def set_imag_param(self, value):
        self.imag.set(value) # パラメータを設定
        self.quick_draw() # 簡易描画

    # --- パラメータ設定用関数（最大反復回数） (ControlPanelから呼び出す) ---
    def set_max_iter_param(self, value):
        self.max_iter.set(value) # パラメータを設定
        self.quick_draw() # 簡易描画

    # --- パラメータ設定用関数（開始色） (ControlPanelから呼び出す) ---
    def set_start_color_param(self, color_hex):
        try: # 16進数のカラーコードを10進数に変換
            if color_map.is_valid_hex_color(color_hex): # 16進数のカラーコードが有効な場合
                self.start_color.set(color_hex)
            else: # 16進数のカラーコードが無効な場合
                self.start_color.set("#0000FF")
        except: # 16進数のカラーコードが無効な場合
            self.start_color.set("#0000FF")
        finally:
            self.quick_draw() # 無条件で再描画

    # --- パラメータ設定用関数（終了色） (ControlPanelから呼び出す) ---
    def set_end_color_param(self, color_hex):
        try:
            if color_map.is_valid_hex_color(color_hex):
                self.end_color.set(color_hex)
            else:
                self.end_color.set("#0000FF")
        except:
            self.end_color.set("#0000FF")
        finally:
            self.quick_draw()
