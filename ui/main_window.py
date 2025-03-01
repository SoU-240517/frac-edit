import tkinter as tk
import numpy as np
from tkinter import ttk
from PIL import Image, ImageTk
from .control_panel import ControlPanel
from core import fractal, color_map

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Julia Set Viewer")
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas_width = 1280
        self.canvas_height = 720
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(side=tk.LEFT)

        self.initial_params = {
            'real': -0.4,
            'imag': 0.6,
            'max_iter': 300,
            'start_color': "#0000FF",
            'end_color': "#FFFFFF",
            'inner_color': "#000000"
        }

        self.real = tk.DoubleVar(value=self.initial_params['real'])
        self.imag = tk.DoubleVar(value=self.initial_params['imag'])
        self.max_iter = tk.IntVar(value=self.initial_params['max_iter'])
        self.start_color = tk.StringVar(value=self.initial_params['start_color'])
        self.end_color = tk.StringVar(value=self.initial_params['end_color'])
        self.inner_color = tk.StringVar(value=self.initial_params['inner_color'])

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
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<Button-4>', self.on_mousewheel)
        self.canvas.bind('<Button-5>', self.on_mousewheel)
        self.canvas.bind('<Button-3>', self.start_pan)
        self.canvas.bind('<B3-Motion>', self.on_pan)
        self.pan_start_x = None
        self.pan_start_y = None
        self.control_panel = ControlPanel(self.main_frame, self)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.quick_draw()

    def quick_draw(self):
        self._draw(quick=True)

    def full_draw(self):
        self._draw(quick=False)

    def _draw(self, quick=False):
        if quick:
            skip = 4
        else:
            skip = 1
        #calculate_julia から返される値を変更
        iterations, potentials = fractal.calculate_julia(
            self.view_x_min, self.view_x_max,
            self.view_y_min, self.view_y_max,
            self.canvas_width, self.canvas_height,
            self.real.get(), self.imag.get(),
            self.max_iter.get(), skip
        )
        #color_map.create_colormapの引数を変更
        colors = color_map.create_colormap(
            iterations, potentials,
            self.start_color.get(),
            self.end_color.get(),
            self.inner_color.get(),
        )
        if quick:
            if len(colors.shape) != 3:
                raise ValueError(f"Invalid colors shape: {colors.shape}, expected (height, width, 3)")
            colors_resized = np.repeat(np.repeat(colors, skip, axis=0), skip, axis=1)
            img = Image.fromarray(colors_resized)
        else:
            img = Image.fromarray(colors)
        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def on_mousewheel(self, event):
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
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def on_pan(self, event):
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

    def reset_view(self):
        self.view_x_min = self.initial_view['x_min']
        self.view_x_max = self.initial_view['x_max']
        self.view_y_min = self.initial_view['y_min']
        self.view_y_max = self.initial_view['y_max']
        self.quick_draw()

    def reset_params(self):
        self.real.set(self.initial_params['real'])
        self.imag.set(self.initial_params['imag'])
        self.max_iter.set(self.initial_params['max_iter'])
        self.start_color.set(self.initial_params['start_color'])
        self.end_color.set(self.initial_params['end_color'])
        self.inner_color.set(self.initial_params['inner_color'])
        self.reset_view()

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
        try:
            if color_map.is_valid_hex_color(color_hex):
                self.start_color.set(color_hex)
            else:
                self.start_color.set(self.initial_params['start_color'])
        except:
            self.start_color.set(self.initial_params['start_color'])
        finally:
            self.quick_draw()

    def set_end_color_param(self, color_hex):
        try:
            if color_map.is_valid_hex_color(color_hex):
                self.end_color.set(color_hex)
            else:
                self.end_color.set("#0000FF")
        except :
            self.end_color.set(self.initial_params['end_color'])
        finally:
            self.quick_draw()

    def set_inner_color_param(self, color_hex): # --- 内部色の値をControlPanelから設定するメソッド ---
        try:
            if color_map.is_valid_hex_color(color_hex):
                self.inner_color.set(color_hex)
            else:
                self.inner_color.set("#000000")
        except :
            self.inner_color.set(self.initial_params['inner_color'])
        finally:
            self.quick_draw()
