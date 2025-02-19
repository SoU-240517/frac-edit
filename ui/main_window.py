# julia_viewer/ui/main_window.py
import tkinter as tk
import numpy as np
from tkinter import ttk
from PIL import Image, ImageTk
from .control_panel import ControlPanel  # ControlPanelクラスのインポート
from core import fractal, color_map # coreモジュールのインポート

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Julia Set Viewer")

        # パラメータの初期値 (ControlPanelに移動しても良い)
        self.real = tk.DoubleVar(value=-0.4)
        self.imag = tk.DoubleVar(value=0.6)
        self.max_iter = tk.IntVar(value=100)
        self.start_color = tk.StringVar(value="#0000FF")  # 青
        self.end_color = tk.StringVar(value="#FFFFFF")    # 白

        # ビュー範囲の初期値
        self.view_x_min = -2.0
        self.view_x_max = 2.0
        self.view_y_min = -2.0
        self.view_y_max = 2.0
        self.initial_view = {
            'x_min': -2.0,
            'x_max': 2.0,
            'y_min': -2.0,
            'y_max': 2.0
        }

        # メインフレームの設定
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # キャンバスの設定
        self.canvas_width = 800
        self.canvas_height = 500
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(side=tk.LEFT)

        # マウスイベントのバインド
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)  # Windows
        self.canvas.bind('<Button-4>', self.on_mousewheel)    # Linux上スクロール
        self.canvas.bind('<Button-5>', self.on_mousewheel)    # Linux下スクロール
        self.canvas.bind('<Button-3>', self.start_pan)      # 右クリック開始
        self.canvas.bind('<B3-Motion>', self.on_pan)        # 右ドラッグ

        # パン用の変数
        self.pan_start_x = None
        self.pan_start_y = None

        # コントロールパネルの設定 (ControlPanelクラスを使用)
        self.control_panel = ControlPanel(self.main_frame, self) # MainWindowを親とselfとして渡す
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        # 初回描画
        self.quick_draw()

    def quick_draw(self):
        self._draw(quick=True)

    def full_draw(self):
        self._draw(quick=False)

    def _draw(self, quick=False):
        """描画処理の共通部分"""
        if quick:
            skip = 4  # 簡易描画の場合は間引く
        else:
            skip = 1

        output = fractal.calculate_julia( # fractalモジュールの関数を使用
            self.view_x_min, self.view_x_max,
            self.view_y_min, self.view_y_max,
            self.canvas_width, self.canvas_height,
            self.real.get(), self.imag.get(),
            self.max_iter.get(), skip
        )

        # カラーマップの適用 (color_mapモジュールの関数を使用)
        colors = color_map.create_colormap(
            output,
            self.start_color.get(),
            self.end_color.get()
        )

        # 画像の拡大 (簡易描画時のみ)
        if quick:
            colors_resized = np.repeat(np.repeat(colors, skip, axis=0), skip, axis=1)
            img = Image.fromarray(colors_resized)
        else:
            img = Image.fromarray(colors)

        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    # --- イベントハンドラ (マウス操作) ---
    def on_mousewheel(self, event):
        # ... (変更なし) ...
        canvas_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        canvas_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        complex_x = self.view_x_min + (self.view_x_max - self.view_x_min) * (canvas_x / self.canvas_width)
        complex_y = self.view_y_min + (self.view_y_max - self.view_y_min) * (canvas_y / self.canvas_height)

        if event.num == 4 or event.delta > 0:
            zoom_factor = 0.9
        else:
            zoom_factor = 1.1

        width = (self.view_x_max - self.view_x_min) * zoom_factor
        height = (self.view_y_max - self.view_y_min) * zoom_factor

        self.view_x_min = complex_x - width * (canvas_x / self.canvas_width)
        self.view_x_max = complex_x + width * (1 - canvas_x / self.canvas_width)
        self.view_y_min = complex_y - height * (canvas_y / self.canvas_height)
        self.view_y_max = complex_y + height * (1 - canvas_y / self.canvas_height)

        self.quick_draw()

    def start_pan(self, event):
        # ... (変更なし) ...
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def on_pan(self, event):
        # ... (変更なし) ...
        if self.pan_start_x is None or self.pan_start_y is None:
            return

        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y

        x_scale = (self.view_x_max - self.view_x_min) / self.canvas_width
        y_scale = (self.view_y_max - self.view_y_min) / self.canvas_height

        dx_complex = -dx * x_scale
        dy_complex = -dy * y_scale

        self.view_x_min += dx_complex
        self.view_x_max += dx_complex
        self.view_y_min += dy_complex
        self.view_y_max += dy_complex

        self.pan_start_x = event.x
        self.pan_start_y = event.y

        self.quick_draw()

    # --- パラメータ操作 ---
    def reset_view(self):
        """ビュー範囲を初期状態に戻す"""
        self.view_x_min = self.initial_view['x_min']
        self.view_x_max = self.initial_view['x_max']
        self.view_y_min = self.initial_view['y_min']
        self.view_y_max = self.initial_view['y_max']
        self.quick_draw()

    def reset_params(self): # ControlPanelに移動しても良い
        """パラメータを初期値に戻す (ビューもリセット)"""
        self.real.set(-0.4)
        self.imag.set(0.6)
        self.max_iter.set(100)
        self.start_color.set("#0000FF")
        self.end_color.set("#FFFFFF")
        self.reset_view()


    # --- パラメータ設定用関数 (ControlPanelから呼び出す) ---
    def set_real_param(self, value):
        self.real.set(value)
        self.quick_draw()

    def set_imag_param(self, value):
        self.imag.set(value)
        self.quick_draw()

    def set_max_iter_param(self, value):
        self.max_iter.set(value)
        self.quick_draw()

    def set_start_color_param(self, color_hex):
        if color_map.is_valid_hex_color(color_hex): # color_mapモジュールの関数を使用
            self.start_color.set(color_hex)
            self.quick_draw()
        else:
            # 無効な色コードの場合はエラー処理 (例: デフォルト色に戻す)
            self.start_color.set("#0000FF") # デフォルトの開始色
            self.quick_draw()
            print("エラー：開始色の形式が正しくありません。デフォルトの色を使用します。")


    def set_end_color_param(self, color_hex):
        if color_map.is_valid_hex_color(color_hex): # color_mapモジュールの関数を使用
            self.end_color.set(color_hex)
            self.quick_draw()
        else:
            # 無効な色コードの場合はエラー処理 (例: デフォルト色に戻す)
            self.end_color.set("#FFFFFF") # デフォルトの終了色
            self.quick_draw()
            print("エラー：終了色の形式が正しくありません。デフォルトの色を使用します。")
