import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk

class JuliaSetViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Julia Set Viewer")
        
        # パラメータの初期値
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
        self.canvas.bind('<Button-3>', self.start_pan)        # 右クリック開始
        self.canvas.bind('<B3-Motion>', self.on_pan)          # 右ドラッグ
        
        # パン用の変数
        self.pan_start_x = None
        self.pan_start_y = None
        self.initial_view = {
            'x_min': -2.0,
            'x_max': 2.0,
            'y_min': -2.0,
            'y_max': 2.0
        }
        
        # コントロールパネルの設定
        self.setup_control_panel()
        
        # 初回描画
        self.quick_draw()

    def setup_control_panel(self):
        # コントロールパネルのフレーム
        control_panel = ttk.Frame(self.main_frame, padding="10")
        control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 実部のコントロール
        ttk.Label(control_panel, text="実部:").pack()
        real_entry = ttk.Entry(control_panel, textvariable=self.real, width=20)
        real_entry.pack()
        real_entry.bind('<Return>', self.on_entry_change)
        real_entry.bind('<FocusOut>', self.on_entry_change)
        real_slider = ttk.Scale(control_panel, from_=-2.0, to=2.0, variable=self.real,
                              orient=tk.HORIZONTAL, command=self.on_slider_change)
        real_slider.pack()
        
        # 虚部のコントロール
        ttk.Label(control_panel, text="虚部:").pack()
        imag_entry = ttk.Entry(control_panel, textvariable=self.imag, width=20)
        imag_entry.pack()
        imag_entry.bind('<Return>', self.on_entry_change)
        imag_entry.bind('<FocusOut>', self.on_entry_change)
        imag_slider = ttk.Scale(control_panel, from_=-2.0, to=2.0, variable=self.imag,
                               orient=tk.HORIZONTAL, command=self.on_slider_change)
        imag_slider.pack()
        
        # 反復回数のコントロール
        ttk.Label(control_panel, text="反復回数:").pack()
        iter_entry = ttk.Entry(control_panel, textvariable=self.max_iter, width=10)
        iter_entry.pack()
        iter_entry.bind('<Return>', self.on_iter_change)  # Enterキーで更新
        iter_entry.bind('<FocusOut>', self.on_iter_change)  # フォーカスを失ったときに更新
        
        # カラーマップのコントロール
        ttk.Label(control_panel, text="開始色:").pack()
        color_frame1 = ttk.Frame(control_panel)
        color_frame1.pack(fill=tk.X, pady=2)
        
        start_color_entry = ttk.Entry(color_frame1, textvariable=self.start_color, width=8)
        start_color_entry.pack(side=tk.LEFT, padx=2)
        start_color_entry.bind('<Return>', self.on_color_change)
        start_color_entry.bind('<FocusOut>', self.on_color_change)
        
        ttk.Button(color_frame1, text="選択", 
                  command=lambda: self.choose_color('start')).pack(side=tk.LEFT)
        
        ttk.Label(control_panel, text="終了色:").pack()
        color_frame2 = ttk.Frame(control_panel)
        color_frame2.pack(fill=tk.X, pady=2)
        
        end_color_entry = ttk.Entry(color_frame2, textvariable=self.end_color, width=8)
        end_color_entry.pack(side=tk.LEFT, padx=2)
        end_color_entry.bind('<Return>', self.on_color_change)
        end_color_entry.bind('<FocusOut>', self.on_color_change)
        
        ttk.Button(color_frame2, text="選択", 
                  command=lambda: self.choose_color('end')).pack(side=tk.LEFT)
        
        # 更新ボタン
        ttk.Button(control_panel, text="更新", command=self.full_draw).pack(pady=10)

        # リセットボタンの追加
        ttk.Button(control_panel, text="リセット", command=self.reset_view).pack(pady=10)

    def on_mousewheel(self, event):
        # マウスポインタの位置を取得（キャンバス座標系）
        canvas_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        canvas_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        
        # キャンバス座標を複素平面座標に変換
        complex_x = self.view_x_min + (self.view_x_max - self.view_x_min) * (canvas_x / self.canvas_width)
        complex_y = self.view_y_min + (self.view_y_max - self.view_y_min) * (canvas_y / self.canvas_height)
        
        # ズーム倍率の決定
        if event.num == 4 or event.delta > 0:  # ズームイン
            zoom_factor = 0.9
        else:  # ズームアウト
            zoom_factor = 1.1
        
        # 新しいビュー範囲の計算
        width = (self.view_x_max - self.view_x_min) * zoom_factor
        height = (self.view_y_max - self.view_y_min) * zoom_factor
        
        # マウス位置を中心にズーム
        self.view_x_min = complex_x - width * (canvas_x / self.canvas_width)
        self.view_x_max = complex_x + width * (1 - canvas_x / self.canvas_width)
        self.view_y_min = complex_y - height * (canvas_y / self.canvas_height)
        self.view_y_max = complex_y + height * (1 - canvas_y / self.canvas_height)
        
        # 簡易描画で更新
        self.quick_draw()

    def start_pan(self, event):
        """パンの開始位置を記録"""
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def on_pan(self, event):
        """パン処理を実行"""
        if self.pan_start_x is None or self.pan_start_y is None:
            return
            
        # 移動量を計算（キャンバス座標系）
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        
        # キャンバス座標系から複素平面座標系への変換係数
        x_scale = (self.view_x_max - self.view_x_min) / self.canvas_width
        y_scale = (self.view_y_max - self.view_y_min) / self.canvas_height
        
        # ビュー範囲の更新
        dx_complex = -dx * x_scale
        dy_complex = -dy * y_scale
        
        self.view_x_min += dx_complex
        self.view_x_max += dx_complex
        self.view_y_min += dy_complex
        self.view_y_max += dy_complex
        
        # 次回の移動量計算用に現在位置を記録
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        
        # 簡易描画で更新
        self.quick_draw()

    def reset_params(self):
        """パラメータを初期値に戻す"""
        self.real.set(-0.4)
        self.imag.set(0.6)
        self.max_iter.set(100)
        self.start_color.set("#0000FF")
        self.end_color.set("#FFFFFF")
        self.reset_view()  # ビューもリセット

    def reset_view(self):
        """ビュー範囲を初期状態に戻す"""
        self.view_x_min = self.initial_view['x_min']
        self.view_x_max = self.initial_view['x_max']
        self.view_y_min = self.initial_view['y_min']
        self.view_y_max = self.initial_view['y_max']
        self.quick_draw()

    def calculate_julia(self, width, height, skip=1):
        x = np.linspace(self.view_x_min, self.view_x_max, width)
        y = np.linspace(self.view_y_min, self.view_y_max, height)
        X, Y = np.meshgrid(x[::skip], y[::skip])
        Z = X + Y*1j
        
        c = complex(self.real.get(), self.imag.get())
        max_iter = self.max_iter.get()
        
        output = np.zeros(Z.shape, dtype=np.float32)
        
        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + c
            output[mask & (np.abs(Z) > 2)] = i + 1 - np.log2(np.log2(np.abs(Z[mask & (np.abs(Z) > 2)])))
        
        # 正規化
        mask = output > 0
        if mask.any():
            output[mask] = (output[mask] - output[mask].min()) / (output[mask].max() - output[mask].min())
        
        return output

    def hex_to_rgb(self, hex_color):
        """16進数カラーコードをRGB値に変換"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def is_valid_hex_color(self, color):
        """16進数カラーコードの形式を検証"""
        if not color.startswith('#'):
            return False
        try:
            int(color[1:], 16)
            return len(color) == 7
        except ValueError:
            return False

    def create_colormap(self, values):
        # 開始色と終了色のRGB値を取得
        try:
            start_rgb = self.hex_to_rgb(self.start_color.get())
            end_rgb = self.hex_to_rgb(self.end_color.get())
        except:
            # エラーの場合はデフォルトの色を使用
            self.start_color.set("#0000FF")
            self.end_color.set("#FFFFFF")
            start_rgb = (0, 0, 255)
            end_rgb = (255, 255, 255)

        colors = np.zeros((values.shape[0], values.shape[1], 3), dtype=np.uint8)
        
        # 値を0-1に正規化
        normalized = np.where(values > 0, values, 0)
        
        # 各色成分に対してグラデーションを計算
        for i in range(3):
            colors[..., i] = start_rgb[i] + normalized * (end_rgb[i] - start_rgb[i])
        
        return colors

    def choose_color(self, color_type):
        """カラーパレットを表示して色を選択"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(
            color=self.start_color.get() if color_type == 'start' else self.end_color.get(),
            title=f"{color_type.capitalize()}色の選択"
        )
        
        if color[1]:  # 色が選択された場合
            if color_type == 'start':
                self.start_color.set(color[1])
            else:
                self.end_color.set(color[1])
            self.quick_draw()

    def on_color_change(self, event):
        """色の入力フィールドが変更された時の処理"""
        start_color = self.start_color.get()
        end_color = self.end_color.get()
        
        # 入力値を検証
        if not self.is_valid_hex_color(start_color):
            self.start_color.set("#0000FF")
        if not self.is_valid_hex_color(end_color):
            self.end_color.set("#FFFFFF")
            
        self.quick_draw()

    def quick_draw(self):
        self.is_quick_draw = True
        skip = 4  # 4点おきに描画
        output = self.calculate_julia(self.canvas_width, self.canvas_height, skip)
        
        # カラーマップの適用
        colors = self.create_colormap(output)
        
        # 画像の拡大
        colors_resized = np.repeat(np.repeat(colors, skip, axis=0), skip, axis=1)
        
        # 描画
        img = Image.fromarray(colors_resized)
        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def full_draw(self):
        output = self.calculate_julia(self.canvas_width, self.canvas_height, skip=1)
        
        # カラーマップの適用
        colors = self.create_colormap(output)
        
        # 描画
        img = Image.fromarray(colors)
        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def on_slider_change(self, _):
        self.quick_draw()
        
    def on_entry_change(self, event):
        try:
            # 入力値を検証
            real = float(self.real.get())
            imag = float(self.imag.get())
            
            # 値の範囲を制限
            self.real.set(max(-2.0, min(2.0, real)))
            self.imag.set(max(-2.0, min(2.0, imag)))
            
            # 描画を更新
            self.quick_draw()
        except ValueError:
            # 無効な入力の場合は以前の値に戻す
            self.real.set(self.real.get())
            self.imag.set(self.imag.get())
            
    def on_iter_change(self, event):
        try:
            # 入力値を検証
            iter_val = int(self.max_iter.get())
            
            # 最小値を1に制限
            self.max_iter.set(max(1, iter_val))
            
            # 描画を更新
            self.quick_draw()
        except ValueError:
            # 無効な入力の場合は以前の値に戻す
            self.max_iter.set(self.max_iter.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = JuliaSetViewer(root)
    root.mainloop()
