"""
フラクタルジェネレータのメインアプリケーション（修正版）

このモジュールは、フラクタルジェネレータのGUIアプリケーションを提供します。
スクロールバーを追加し、'complex' object is not subscriptableエラーを修正しています。
"""

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
import numpy as np
import os
import json
from PIL import Image, ImageTk
import threading
import time

# コアモジュールをインポート
from src.core import (
    FractalBase, MandelbrotJulia, PluginManager,
    IterationColoring, ContinuousPotentialColoring, GradientGenerator,
    FractalRenderer
)

class FractalGeneratorApp:
    """
    フラクタルジェネレータのメインアプリケーションクラス
    """
    
    def __init__(self, root):
        """
        初期化メソッド
        
        Args:
            root (tk.Tk): Tkinterのルートウィンドウ
        """
        self.root = root
        self.root.title("フラクタルジェネレータ")
        self.root.geometry("1400x900")
        
        # 状態変数
        self.current_fractal = None
        self.current_coloring = None
        self.current_gradient = None
        self.current_view = {
            'x_min': -2.0,
            'x_max': 1.0,
            'y_min': -1.5,
            'y_max': 1.5
        }
        self.canvas_mode = True  # True: キャンバスモード, False: ノード編集モード
        self.frames = []  # フレームのリスト
        self.current_frame_index = 0
        
        # プラグインマネージャーを初期化
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        
        # レンダラーを初期化
        self.renderer = FractalRenderer(800, 600)
        
        # デフォルトのフラクタルとカラーリングを設定
        self.current_fractal = MandelbrotJulia(800, 600)
        self.current_coloring = IterationColoring()
        self.current_gradient = GradientGenerator.create_preset_gradients()['rainbow']
        
        # 履歴管理
        self.history = []
        self.history_position = -1
        self.max_history = 50
        
        # UIコンポーネントを作成
        self.create_widgets()
        
        # 初期フレームを追加
        self.add_frame()
        
        # 初期描画
        self.render_fractal()
    
    def create_widgets(self):
        """
        UIコンポーネントを作成するメソッド
        """
        # --- メインフレーム ---
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # --- 左: コンテンツ領域 / 右: 操作パネル ---
        self.content_area = tk.Frame(self.main_frame, bg="white")
        
        # スクロール可能なコントロールパネルコンテナを作成
        self.control_panel_container = tk.Frame(self.main_frame, bg="lightgray", width=500)
        self.control_panel_container.grid_propagate(False)
        
        # スクロールバーを追加
        self.scrollbar = tk.Scrollbar(self.control_panel_container, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        
        # キャンバスを使ってスクロール可能にする
        self.control_canvas = tk.Canvas(self.control_panel_container, 
                                       yscrollcommand=self.scrollbar.set,
                                       bg="lightgray")
        self.control_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.control_canvas.yview)
        
        # 実際のコントロールパネル
        self.control_panel = tk.Frame(self.control_canvas, bg="lightgray")
        self.control_panel_window = self.control_canvas.create_window((0, 0), 
                                                                     window=self.control_panel, 
                                                                     anchor="nw")
        
        # フレームサイズが変わったときにスクロール領域を更新
        self.control_panel.bind("<Configure>", 
                               lambda e: self.control_canvas.configure(
                                   scrollregion=self.control_canvas.bbox("all")))
        
        # マウスホイールでスクロールできるようにする
        self.control_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.control_canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.control_canvas.bind_all("<Button-5>", self._on_mousewheel)
        
        self.content_area.grid(row=0, column=0, sticky="nsew")
        self.control_panel_container.grid(row=0, column=1, sticky="ns")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # --- コンテンツ領域のコンポーネント ---
        # キャンバス
        self.canvas_frame = tk.Frame(self.content_area, bg="black")
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # キャンバスイベント
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<MouseWheel>", self.on_canvas_wheel)  # Windows
        self.canvas.bind("<Button-4>", self.on_canvas_wheel)    # Linux上スクロール
        self.canvas.bind("<Button-5>", self.on_canvas_wheel)    # Linux下スクロール
        
        # ノードエディタ（初期状態では非表示）
        self.node_editor_frame = tk.Frame(self.content_area, bg="darkgray")
        
        # === 操作パネル内のウィジェット（上から順に配置） ===
        # 1. キャンバスビュー（ミニマップ）
        self.minimap_frame = tk.Frame(self.control_panel, bg="black", height=200)
        self.minimap_frame.grid(row=0, column=0, padx=3, pady=(3,0), sticky="ew")
        self.minimap_frame.grid_propagate(False)
        
        self.minimap_canvas = tk.Canvas(self.minimap_frame, bg="black", highlightthickness=0)
        self.minimap_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 2. キャンバス／ノード切替ボタン
        self.toggle_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.toggle_frame.grid(row=1, column=0, padx=3, pady=(3,0), sticky="ew")
        self.canvas_button = tk.Button(self.toggle_frame, text="キャンバス", command=self.switch_to_canvas)
        self.canvas_button.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.node_button = tk.Button(self.toggle_frame, text="ノード編集", command=self.switch_to_node_editor)
        self.node_button.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.toggle_frame.columnconfigure(0, weight=1)
        self.toggle_frame.columnconfigure(1, weight=1)
        
        # 3. パラメータセーブ／ロードボタン
        self.save_load_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.save_load_frame.grid(row=2, column=0, padx=3, pady=(3,0), sticky="ew")
        self.param_save_button = tk.Button(self.save_load_frame, text="パラメータセーブ", command=self.save_parameters)
        self.param_save_button.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.param_load_button = tk.Button(self.save_load_frame, text="パラメータロード", command=self.load_parameters)
        self.param_load_button.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.save_load_frame.columnconfigure(0, weight=1)
        self.save_load_frame.columnconfigure(1, weight=1)
        
        # 4. ズーム操作ボタン
        self.zoom_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.zoom_frame.grid(row=3, column=0, padx=3, pady=(3,0), sticky="ew")
        self.zoom_in_button = tk.Button(self.zoom_frame, text="ズームイン", command=lambda: self.zoom(0.5))
        self.zoom_in_button.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.zoom_out_button = tk.Button(self.zoom_frame, text="ズームアウト", command=lambda: self.zoom(2.0))
        self.zoom_out_button.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.reset_view_button = tk.Button(self.zoom_frame, text="ビューリセット", command=self.reset_view)
        self.reset_view_button.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky="ew")
        self.zoom_frame.columnconfigure(0, weight=1)
        self.zoom_frame.columnconfigure(1, weight=1)
        
        # 5. マイフレーム選択
        self.myframe_select_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.myframe_select_frame.grid(row=4, column=0, padx=3, pady=(3,0), sticky="ew")
        self.prev_frame_button = tk.Button(self.myframe_select_frame, text="前のフレーム", command=self.prev_frame)
        self.prev_frame_button.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.next_frame_button = tk.Button(self.myframe_select_frame, text="次のフレーム", command=self.next_frame)
        self.next_frame_button.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.add_frame_button = tk.Button(self.myframe_select_frame, text="フレーム追加", command=self.add_frame)
        self.add_frame_button.grid(row=1, column=0, padx=3, pady=3, sticky="ew")
        self.del_frame_button = tk.Button(self.myframe_select_frame, text="フレーム削除", command=self.delete_frame)
        self.del_frame_button.grid(row=1, column=1, padx=3, pady=3, sticky="ew")
        self.myframe_select_frame.columnconfigure(0, weight=1)
        self.myframe_select_frame.columnconfigure(1, weight=1)
        
        # 6. フラクタルタイプ選択
        self.frac_type_dropdown_var = tk.StringVar()
        self.frac_type_dropdown_var.set("マンデルブロ集合")
        self.frac_type_combobox = ttk.Combobox(self.control_panel, textvariable=self.frac_type_dropdown_var,
                                              values=["マンデルブロ集合", "ジュリア集合"])
        self.frac_type_combobox.grid(row=5, column=0, padx=3, pady=(3,0), sticky="ew")
        self.frac_type_combobox.bind("<<ComboboxSelected>>", self.on_fractal_type_change)
        
        # 7. フレームリスト
        self.tree = ttk.Treeview(self.control_panel, columns=("frame", "ftype"), show="headings", height=5)
        self.tree.grid(row=6, column=0, padx=3, pady=(3,0), sticky="ew")
        self.tree.heading("frame", text="フレーム")
        self.tree.heading("ftype", text="タイプ")
        self.tree.column("frame", width=100)
        self.tree.column("ftype", width=150)
        self.tree.bind("<<TreeviewSelect>>", self.on_frame_select)
        
        # 8. パラメータ設定（フラクタルタイプ別）
        # マンデルブロ/ジュリア用パラメータ
        self.plugin_frame1 = tk.Frame(self.control_panel, bg="darkgray")
        self.plugin_frame1.grid(row=7, column=0, padx=3, pady=(3,0), sticky="ew")
        
        # 最大反復回数
        tk.Label(self.plugin_frame1, text="最大反復回数:").grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.max_iter_var = tk.StringVar(value="100")
        self.max_iter_entry = tk.Entry(self.plugin_frame1, textvariable=self.max_iter_var, width=10)
        self.max_iter_entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        
        # 発散半径
        tk.Label(self.plugin_frame1, text="発散半径:").grid(row=1, column=0, padx=3, pady=3, sticky="w")
        self.escape_radius_var = tk.StringVar(value="2.0")
        self.escape_radius_entry = tk.Entry(self.plugin_frame1, textvariable=self.escape_radius_var, width=10)
        self.escape_radius_entry.grid(row=1, column=1, padx=3, pady=3, sticky="ew")
        
        # ジュリア集合のcパラメータ
        tk.Label(self.plugin_frame1, text="c実部:").grid(row=2, column=0, padx=3, pady=3, sticky="w")
        self.c_real_var = tk.StringVar(value="-0.7")
        self.c_real_entry = tk.Entry(self.plugin_frame1, textvariable=self.c_real_var, width=10)
        self.c_real_entry.grid(row=2, column=1, padx=3, pady=3, sticky="ew")
        
        tk.Label(self.plugin_frame1, text="c虚部:").grid(row=3, column=0, padx=3, pady=3, sticky="w")
        self.c_imag_var = tk.StringVar(value="0.27015")
        self.c_imag_entry = tk.Entry(self.plugin_frame1, textvariable=self.c_imag_var, width=10)
        self.c_imag_entry.grid(row=3, column=1, padx=3, pady=3, sticky="ew")
        
        # パラメータ適用ボタン
        self.apply_params_button = tk.Button(self.plugin_frame1, text="パラメータ適用", command=self.apply_parameters)
        self.apply_params_button.grid(row=4, column=0, columnspan=2, padx=3, pady=3, sticky="ew")
        
        # 9. トランスフォーム設定
        self.plugin_frame2 = tk.Frame(self.control_panel, bg="darkgray")
        self.plugin_frame2.grid(row=8, column=0, padx=3, pady=(3,0), sticky="ew")
        
        # ピボットX
        tk.Label(self.plugin_frame2, text="ピボットX:").grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.pivot_x_var = tk.StringVar(value="0.0")
        self.pivot_x_entry = tk.Entry(self.plugin_frame2, textvariable=self.pivot_x_var, width=10)
        self.pivot_x_entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        
        # ピボットY
        tk.Label(self.plugin_frame2, text="ピボットY:").grid(row=1, column=0, padx=3, pady=3, sticky="w")
        self.pivot_y_var = tk.StringVar(value="0.0")
        self.pivot_y_entry = tk.Entry(self.plugin_frame2, textvariable=self.pivot_y_var, width=10)
        self.pivot_y_entry.grid(row=1, column=1, padx=3, pady=3, sticky="ew")
        
        # 回転角度
        tk.Label(self.plugin_frame2, text="回転角度:").grid(row=2, column=0, padx=3, pady=3, sticky="w")
        self.rotation_var = tk.StringVar(value="0.0")
        self.rotation_entry = tk.Entry(self.plugin_frame2, textvariable=self.rotation_var, width=10)
        self.rotation_entry.grid(row=2, column=1, padx=3, pady=3, sticky="ew")
        
        # スケールX
        tk.Label(self.plugin_frame2, text="スケールX:").grid(row=3, column=0, padx=3, pady=3, sticky="w")
        self.scale_x_var = tk.StringVar(value="1.0")
        self.scale_x_entry = tk.Entry(self.plugin_frame2, textvariable=self.scale_x_var, width=10)
        self.scale_x_entry.grid(row=3, column=1, padx=3, pady=3, sticky="ew")
        
        # スケールY
        tk.Label(self.plugin_frame2, text="スケールY:").grid(row=4, column=0, padx=3, pady=3, sticky="w")
        self.scale_y_var = tk.StringVar(value="1.0")
        self.scale_y_entry = tk.Entry(self.plugin_frame2, textvariable=self.scale_y_var, width=10)
        self.scale_y_entry.grid(row=4, column=1, padx=3, pady=3, sticky="ew")
        
        # トランスフォーム適用ボタン
        self.apply_transform_button = tk.Button(self.plugin_frame2, text="トランスフォーム適用", command=self.apply_transform)
        self.apply_transform_button.grid(row=5, column=0, columnspan=2, padx=3, pady=3, sticky="ew")
        
        # 10. カラー設定
        self.color_set_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.color_set_frame.grid(row=9, column=0, padx=3, pady=(3,0), sticky="ew")
        
        # カラーリングアルゴリズム選択
        tk.Label(self.color_set_frame, text="カラーリング:").grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.coloring_var = tk.StringVar(value="反復回数")
        self.coloring_combobox = ttk.Combobox(self.color_set_frame, textvariable=self.coloring_var,
                                             values=["反復回数", "連続ポテンシャル"])
        self.coloring_combobox.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.coloring_combobox.bind("<<ComboboxSelected>>", self.on_coloring_change)
        
        # グラデーションプリセット選択
        tk.Label(self.color_set_frame, text="グラデーション:").grid(row=1, column=0, padx=3, pady=3, sticky="w")
        self.gradient_var = tk.StringVar(value="rainbow")
        self.gradient_combobox = ttk.Combobox(self.color_set_frame, textvariable=self.gradient_var,
                                             values=["rainbow", "fire", "ice", "grayscale", "sepia"])
        self.gradient_combobox.grid(row=1, column=1, padx=3, pady=3, sticky="ew")
        self.gradient_combobox.bind("<<ComboboxSelected>>", self.on_gradient_change)
        
        # カラーサイクル
        tk.Label(self.color_set_frame, text="カラーサイクル:").grid(row=2, column=0, padx=3, pady=3, sticky="w")
        self.color_cycle_var = tk.StringVar(value="1.0")
        self.color_cycle_entry = tk.Entry(self.color_set_frame, textvariable=self.color_cycle_var, width=10)
        self.color_cycle_entry.grid(row=2, column=1, padx=3, pady=3, sticky="ew")
        
        # カラーオフセット
        tk.Label(self.color_set_frame, text="カラーオフセット:").grid(row=3, column=0, padx=3, pady=3, sticky="w")
        self.color_offset_var = tk.StringVar(value="0.0")
        self.color_offset_entry = tk.Entry(self.color_set_frame, textvariable=self.color_offset_var, width=10)
        self.color_offset_entry.grid(row=3, column=1, padx=3, pady=3, sticky="ew")
        
        # カラー設定適用ボタン
        self.apply_color_button = tk.Button(self.color_set_frame, text="カラー設定適用", command=self.apply_color_settings)
        self.apply_color_button.grid(row=4, column=0, columnspan=2, padx=3, pady=3, sticky="ew")
        
        # 11. レンダリングボタン
        self.render_button = tk.Button(self.control_panel, text="レンダリング", command=self.render_fractal)
        self.render_button.grid(row=10, column=0, padx=3, pady=(3,0), sticky="ew")
        
        # 12. 高解像度レンダリングボタン
        self.high_res_button = tk.Button(self.control_panel, text="高解像度レンダリング", command=self.render_high_resolution)
        self.high_res_button.grid(row=11, column=0, padx=3, pady=(3,0), sticky="ew")
        
        # 13. 履歴操作ボタン
        self.history_frame = tk.Frame(self.control_panel, bg="darkgray")
        self.history_frame.grid(row=12, column=0, padx=3, pady=(3,0), sticky="ew")
        self.undo_button = tk.Button(self.history_frame, text="元に戻す", command=self.undo)
        self.undo_button.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.redo_button = tk.Button(self.history_frame, text="やり直す", command=self.redo)
        self.redo_button.grid(row=0, column=1, padx=3, pady=3, sticky="ew")
        self.history_frame.columnconfigure(0, weight=1)
        self.history_frame.columnconfigure(1, weight=1)
        
        # 14. ステータスバー
        self.status_var = tk.StringVar(value="準備完了")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky="ew")
        
        # コントロールパネルの列設定
        self.control_panel.columnconfigure(0, weight=1)
    
    def _on_mousewheel(self, event):
        """
        マウスホイールイベントハンドラ（コントロールパネルのスクロール用）
        
        Args:
            event: マウスホイールイベント
        """
        # Windowsの場合
        if event.num == 5 or event.delta < 0:
            self.control_canvas.yview_scroll(1, "units")
        # Linuxの場合
        elif event.num == 4 or event.delta > 0:
            self.control_canvas.yview_scroll(-1, "units")
    
    # 以下、他のメソッドは元のコードと同じ
    def on_canvas_click(self, event):
        """キャンバスクリックイベントハンドラ"""
        self.last_x = event.x
        self.last_y = event.y
    
    def on_canvas_drag(self, event):
        """キャンバスドラッグイベントハンドラ"""
        # パンの実装
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.last_x = event.x
        self.last_y = event.y
        
        # ビューの更新
        width = self.current_view['x_max'] - self.current_view['x_min']
        height = self.current_view['y_max'] - self.current_view['y_min']
        
        dx_view = dx * width / self.canvas.winfo_width()
        dy_view = dy * height / self.canvas.winfo_height()
        
        self.current_view['x_min'] -= dx_view
        self.current_view['x_max'] -= dx_view
        self.current_view['y_min'] += dy_view
        self.current_view['y_max'] += dy_view
        
        # 再描画
        self.render_fractal()
    
    def on_canvas_release(self, event):
        """キャンバスリリースイベントハンドラ"""
        # 履歴に追加
        self.add_to_history()
    
    def on_canvas_wheel(self, event):
        """キャンバスホイールイベントハンドラ（ズーム用）"""
        # ズーム係数
        if event.num == 5 or event.delta < 0:
            factor = 1.1  # ズームアウト
        else:
            factor = 0.9  # ズームイン
        
        # マウス位置を中心にズーム
        self.zoom_at_point(factor, event.x, event.y)
    
    def zoom_at_point(self, factor, x, y):
        """
        指定した点を中心にズームする
        
        Args:
            factor (float): ズーム係数（1より大きいとズームアウト、小さいとズームイン）
            x (int): ズーム中心のX座標（キャンバス上の座標）
            y (int): ズーム中心のY座標（キャンバス上の座標）
        """
        # キャンバス座標から複素平面上の座標に変換
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        width = self.current_view['x_max'] - self.current_view['x_min']
        height = self.current_view['y_max'] - self.current_view['y_min']
        
        # キャンバス上の相対位置（0～1）
        rel_x = x / canvas_width
        rel_y = y / canvas_height
        
        # 複素平面上の座標
        center_x = self.current_view['x_min'] + width * rel_x
        center_y = self.current_view['y_max'] - height * rel_y
        
        # 新しいビューの計算
        new_width = width * factor
        new_height = height * factor
        
        self.current_view['x_min'] = center_x - new_width * rel_x
        self.current_view['x_max'] = center_x + new_width * (1 - rel_x)
        self.current_view['y_min'] = center_y - new_height * (1 - rel_y)
        self.current_view['y_max'] = center_y + new_height * rel_y
        
        # 再描画
        self.render_fractal()
        
        # 履歴に追加
        self.add_to_history()
    
    def zoom(self, factor):
        """
        中央を中心にズームする
        
        Args:
            factor (float): ズーム係数（1より大きいとズームアウト、小さいとズームイン）
        """
        # キャンバスの中央を取得
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # 中央を中心にズーム
        self.zoom_at_point(factor, canvas_width/2, canvas_height/2)
    
    def reset_view(self):
        """ビューをリセットする"""
        self.current_view = {
            'x_min': -2.0,
            'x_max': 1.0,
            'y_min': -1.5,
            'y_max': 1.5
        }
        
        # 再描画
        self.render_fractal()
        
        # 履歴に追加
        self.add_to_history()
    
    def switch_to_canvas(self):
        """キャンバスモードに切り替える"""
        if not self.canvas_mode:
            self.canvas_mode = True
            self.node_editor_frame.grid_forget()
            self.canvas_frame.grid(row=0, column=0, sticky="nsew")
            
            # 再描画
            self.render_fractal()
    
    def switch_to_node_editor(self):
        """ノード編集モードに切り替える"""
        if self.canvas_mode:
            self.canvas_mode = False
            self.canvas_frame.grid_forget()
            self.node_editor_frame.grid(row=0, column=0, sticky="nsew")
            
            # ノードエディタの初期化
            self.init_node_editor()
    
    def init_node_editor(self):
        """ノードエディタを初期化する"""
        # ノードエディタの実装（将来的な拡張）
        pass
    
    def on_fractal_type_change(self, event):
        """フラクタルタイプ変更イベントハンドラ"""
        fractal_type = self.frac_type_dropdown_var.get()
        
        if fractal_type == "マンデルブロ集合":
            self.current_fractal.params['is_julia'] = False
        elif fractal_type == "ジュリア集合":
            self.current_fractal.params['is_julia'] = True
        
        # 再描画
        self.render_fractal()
        
        # 履歴に追加
        self.add_to_history()
    
    def on_coloring_change(self, event):
        """カラーリングアルゴリズム変更イベントハンドラ"""
        coloring_type = self.coloring_var.get()
        
        if coloring_type == "反復回数":
            self.current_coloring = IterationColoring()
        elif coloring_type == "連続ポテンシャル":
            self.current_coloring = ContinuousPotentialColoring()
        
        # 再描画
        self.render_fractal()
        
        # 履歴に追加
        self.add_to_history()
    
    def on_gradient_change(self, event):
        """グラデーション変更イベントハンドラ"""
        gradient_name = self.gradient_var.get()
        gradients = GradientGenerator.create_preset_gradients()
        
        if gradient_name in gradients:
            self.current_gradient = gradients[gradient_name]
        
        # 再描画
        self.render_fractal()
        
        # 履歴に追加
        self.add_to_history()
    
    def apply_parameters(self):
        """パラメータを適用する"""
        try:
            # 入力値を取得
            max_iter = int(self.max_iter_var.get())
            escape_radius = float(self.escape_radius_var.get())
            c_real = float(self.c_real_var.get())
            c_imag = float(self.c_imag_var.get())
            
            # パラメータを設定
            self.current_fractal.params['max_iter'] = max_iter
            self.current_fractal.params['escape_radius'] = escape_radius
            self.current_fractal.params['c_real'] = c_real
            self.current_fractal.params['c_imag'] = c_imag
            
            # 再描画
            self.render_fractal()
            
            # 履歴に追加
            self.add_to_history()
            
        except ValueError:
            messagebox.showerror("エラー", "無効な入力値です。数値を入力してください。")
    
    def apply_transform(self):
        """トランスフォームを適用する"""
        # トランスフォームの実装（将来的な拡張）
        try:
            # 入力値を取得
            pivot_x = float(self.pivot_x_var.get())
            pivot_y = float(self.pivot_y_var.get())
            rotation = float(self.rotation_var.get())
            scale_x = float(self.scale_x_var.get())
            scale_y = float(self.scale_y_var.get())
            
            # トランスフォームを適用（簡易実装）
            # 実際のトランスフォーム処理はより複雑になる
            
            # 再描画
            self.render_fractal()
            
            # 履歴に追加
            self.add_to_history()
            
        except ValueError:
            messagebox.showerror("エラー", "無効な入力値です。数値を入力してください。")
    
    def apply_color_settings(self):
        """カラー設定を適用する"""
        try:
            # 入力値を取得
            color_cycle = float(self.color_cycle_var.get())
            color_offset = float(self.color_offset_var.get())
            
            # カラー設定を適用
            # 実際のカラー処理はより複雑になる
            
            # 再描画
            self.render_fractal()
            
            # 履歴に追加
            self.add_to_history()
            
        except ValueError:
            messagebox.showerror("エラー", "無効な入力値です。数値を入力してください。")
    
    def render_fractal(self):
        """フラクタルをレンダリングする"""
        try:
            # ステータス更新
            self.status_var.set("レンダリング中...")
            self.root.update_idletasks()
            
            # キャンバスサイズを取得
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # サイズが0の場合は処理しない
            if canvas_width <= 0 or canvas_height <= 0:
                return
            
            # フラクタルのサイズを更新
            self.current_fractal.resize(canvas_width, canvas_height)
            
            # フラクタル計算
            result = self.current_fractal.calculate(
                self.current_view['x_min'],
                self.current_view['x_max'],
                self.current_view['y_min'],
                self.current_view['y_max']
            )
            
            # レンダリング
            self.renderer.resize(canvas_width, canvas_height)
            image = self.renderer.render(result, self.current_coloring, self.current_gradient)
            
            # 画像をキャンバスに表示
            self.tk_image = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            
            # ミニマップにも表示
            minimap_width = self.minimap_canvas.winfo_width()
            minimap_height = self.minimap_canvas.winfo_height()
            
            if minimap_width > 0 and minimap_height > 0:
                minimap_image = image.resize((minimap_width, minimap_height), Image.LANCZOS)
                self.minimap_tk_image = ImageTk.PhotoImage(image=minimap_image)
                self.minimap_canvas.create_image(0, 0, anchor=tk.NW, image=self.minimap_tk_image)
            
            # ステータス更新
            self.status_var.set("レンダリング完了")
            
        except Exception as e:
            # エラーメッセージを表示
            self.status_var.set(f"エラー: {str(e)}")
    
    def render_high_resolution(self):
        """高解像度レンダリングを実行する"""
        # 保存先を選択
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG画像", "*.png"), ("JPEG画像", "*.jpg"), ("すべてのファイル", "*.*")]
        )
        
        if not file_path:
            return
        
        # 解像度設定ダイアログ
        dialog = tk.Toplevel(self.root)
        dialog.title("高解像度レンダリング設定")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="幅:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        width_var = tk.StringVar(value="1920")
        width_entry = tk.Entry(dialog, textvariable=width_var)
        width_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="高さ:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        height_var = tk.StringVar(value="1080")
        height_entry = tk.Entry(dialog, textvariable=height_var)
        height_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(dialog, text="オーバーサンプリング:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        oversample_var = tk.StringVar(value="2")
        oversample_entry = tk.Entry(dialog, textvariable=oversample_var)
        oversample_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # 実行関数
        def execute():
            try:
                width = int(width_var.get())
                height = int(height_var.get())
                oversample = int(oversample_var.get())
                
                dialog.destroy()
                
                # プログレスバーダイアログ
                progress_dialog = tk.Toplevel(self.root)
                progress_dialog.title("レンダリング中...")
                progress_dialog.geometry("300x100")
                progress_dialog.transient(self.root)
                progress_dialog.grab_set()
                
                tk.Label(progress_dialog, text="高解像度レンダリングを実行中...").pack(pady=10)
                progress = ttk.Progressbar(progress_dialog, mode="indeterminate")
                progress.pack(fill=tk.X, padx=10, pady=10)
                progress.start()
                
                # バックグラウンドでレンダリング
                def render_task():
                    try:
                        # フラクタルのサイズを更新
                        fractal_copy = MandelbrotJulia(width, height)
                        fractal_copy.params = self.current_fractal.params.copy()
                        
                        # フラクタル計算
                        result = fractal_copy.calculate(
                            self.current_view['x_min'],
                            self.current_view['x_max'],
                            self.current_view['y_min'],
                            self.current_view['y_max']
                        )
                        
                        # レンダリング
                        renderer = FractalRenderer(width, height)
                        image = renderer.render(
                            result, 
                            self.current_coloring, 
                            self.current_gradient,
                            oversample=oversample
                        )
                        
                        # 画像を保存
                        image.save(file_path)
                        
                        # 完了メッセージ
                        self.root.after(0, lambda: [
                            progress_dialog.destroy(),
                            messagebox.showinfo("完了", "高解像度レンダリングが完了しました。")
                        ])
                        
                    except Exception as e:
                        # エラーメッセージ
                        self.root.after(0, lambda: [
                            progress_dialog.destroy(),
                            messagebox.showerror("エラー", f"レンダリング中にエラーが発生しました: {str(e)}")
                        ])
                
                # スレッドでレンダリングを実行
                threading.Thread(target=render_task, daemon=True).start()
                
            except ValueError:
                messagebox.showerror("エラー", "無効な入力値です。数値を入力してください。")
        
        # ボタン
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(button_frame, text="キャンセル", command=dialog.destroy).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="実行", command=execute).grid(row=0, column=1, padx=5)
    
    def save_parameters(self):
        """パラメータを保存する"""
        # 保存先を選択
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSONファイル", "*.json"), ("すべてのファイル", "*.*")]
        )
        
        if not file_path:
            return
        
        # 保存するデータを準備
        data = {
            'fractal_params': self.current_fractal.params,
            'view': self.current_view,
            'coloring': self.coloring_var.get(),
            'gradient': self.gradient_var.get()
        }
        
        # JSONとして保存
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            messagebox.showinfo("完了", "パラメータを保存しました。")
            
        except Exception as e:
            messagebox.showerror("エラー", f"保存中にエラーが発生しました: {str(e)}")
    
    def load_parameters(self):
        """パラメータを読み込む"""
        # ファイルを選択
        file_path = filedialog.askopenfilename(
            filetypes=[("JSONファイル", "*.json"), ("すべてのファイル", "*.*")]
        )
        
        if not file_path:
            return
        
        # JSONから読み込み
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # パラメータを適用
            if 'fractal_params' in data:
                self.current_fractal.params = data['fractal_params']
                
                # UI更新
                self.max_iter_var.set(str(self.current_fractal.params.get('max_iter', 100)))
                self.escape_radius_var.set(str(self.current_fractal.params.get('escape_radius', 2.0)))
                self.c_real_var.set(str(self.current_fractal.params.get('c_real', -0.7)))
                self.c_imag_var.set(str(self.current_fractal.params.get('c_imag', 0.27015)))
                
                # フラクタルタイプ更新
                if self.current_fractal.params.get('is_julia', False):
                    self.frac_type_dropdown_var.set("ジュリア集合")
                else:
                    self.frac_type_dropdown_var.set("マンデルブロ集合")
            
            # ビュー更新
            if 'view' in data:
                self.current_view = data['view']
            
            # カラーリング更新
            if 'coloring' in data:
                self.coloring_var.set(data['coloring'])
                self.on_coloring_change(None)
            
            # グラデーション更新
            if 'gradient' in data:
                self.gradient_var.set(data['gradient'])
                self.on_gradient_change(None)
            
            # 再描画
            self.render_fractal()
            
            # 履歴に追加
            self.add_to_history()
            
            messagebox.showinfo("完了", "パラメータを読み込みました。")
            
        except Exception as e:
            messagebox.showerror("エラー", f"読み込み中にエラーが発生しました: {str(e)}")
    
    def add_frame(self):
        """新しいフレームを追加する"""
        # 現在の状態をコピー
        frame = {
            'fractal_params': self.current_fractal.params.copy(),
            'view': self.current_view.copy(),
            'coloring': self.coloring_var.get(),
            'gradient': self.gradient_var.get()
        }
        
        # フレームリストに追加
        self.frames.append(frame)
        self.current_frame_index = len(self.frames) - 1
        
        # ツリービューを更新
        self.update_frame_tree()
    
    def delete_frame(self):
        """現在のフレームを削除する"""
        if len(self.frames) <= 1:
            messagebox.showinfo("情報", "最後のフレームは削除できません。")
            return
        
        # 現在のフレームを削除
        del self.frames[self.current_frame_index]
        
        # インデックスを調整
        if self.current_frame_index >= len(self.frames):
            self.current_frame_index = len(self.frames) - 1
        
        # フレームを適用
        self.apply_frame(self.current_frame_index)
        
        # ツリービューを更新
        self.update_frame_tree()
    
    def prev_frame(self):
        """前のフレームに移動する"""
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.apply_frame(self.current_frame_index)
    
    def next_frame(self):
        """次のフレームに移動する"""
        if self.current_frame_index < len(self.frames) - 1:
            self.current_frame_index += 1
            self.apply_frame(self.current_frame_index)
    
    def on_frame_select(self, event):
        """フレーム選択イベントハンドラ"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            index = int(item['values'][0]) - 1
            self.current_frame_index = index
            self.apply_frame(index)
    
    def apply_frame(self, index):
        """指定したインデックスのフレームを適用する"""
        if 0 <= index < len(self.frames):
            frame = self.frames[index]
            
            # パラメータを適用
            self.current_fractal.params = frame['fractal_params'].copy()
            self.current_view = frame['view'].copy()
            
            # UI更新
            self.max_iter_var.set(str(self.current_fractal.params.get('max_iter', 100)))
            self.escape_radius_var.set(str(self.current_fractal.params.get('escape_radius', 2.0)))
            self.c_real_var.set(str(self.current_fractal.params.get('c_real', -0.7)))
            self.c_imag_var.set(str(self.current_fractal.params.get('c_imag', 0.27015)))
            
            # フラクタルタイプ更新
            if self.current_fractal.params.get('is_julia', False):
                self.frac_type_dropdown_var.set("ジュリア集合")
            else:
                self.frac_type_dropdown_var.set("マンデルブロ集合")
            
            # カラーリング更新
            self.coloring_var.set(frame['coloring'])
            self.on_coloring_change(None)
            
            # グラデーション更新
            self.gradient_var.set(frame['gradient'])
            self.on_gradient_change(None)
            
            # 再描画
            self.render_fractal()
            
            # ツリービューの選択を更新
            self.update_tree_selection()
    
    def update_frame_tree(self):
        """フレームツリービューを更新する"""
        # ツリービューをクリア
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # フレームを追加
        for i, frame in enumerate(self.frames):
            fractal_type = "ジュリア集合" if frame['fractal_params'].get('is_julia', False) else "マンデルブロ集合"
            self.tree.insert("", "end", values=(i+1, fractal_type))
        
        # 選択を更新
        self.update_tree_selection()
    
    def update_tree_selection(self):
        """ツリービューの選択を更新する"""
        for i, item in enumerate(self.tree.get_children()):
            if i == self.current_frame_index:
                self.tree.selection_set(item)
                self.tree.see(item)
                break
    
    def add_to_history(self):
        """現在の状態を履歴に追加する"""
        # 現在の状態をコピー
        state = {
            'fractal_params': self.current_fractal.params.copy(),
            'view': self.current_view.copy(),
            'coloring': self.coloring_var.get(),
            'gradient': self.gradient_var.get(),
            'frames': [frame.copy() for frame in self.frames],
            'current_frame_index': self.current_frame_index
        }
        
        # 履歴位置以降の履歴を削除
        if self.history_position < len(self.history) - 1:
            self.history = self.history[:self.history_position + 1]
        
        # 履歴に追加
        self.history.append(state)
        self.history_position = len(self.history) - 1
        
        # 履歴の最大数を制限
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            self.history_position = len(self.history) - 1
    
    def undo(self):
        """操作を元に戻す"""
        if self.history_position > 0:
            self.history_position -= 1
            self.apply_history_state(self.history[self.history_position])
    
    def redo(self):
        """操作をやり直す"""
        if self.history_position < len(self.history) - 1:
            self.history_position += 1
            self.apply_history_state(self.history[self.history_position])
    
    def apply_history_state(self, state):
        """履歴の状態を適用する"""
        # パラメータを適用
        self.current_fractal.params = state['fractal_params'].copy()
        self.current_view = state['view'].copy()
        
        # UI更新
        self.max_iter_var.set(str(self.current_fractal.params.get('max_iter', 100)))
        self.escape_radius_var.set(str(self.current_fractal.params.get('escape_radius', 2.0)))
        self.c_real_var.set(str(self.current_fractal.params.get('c_real', -0.7)))
        self.c_imag_var.set(str(self.current_fractal.params.get('c_imag', 0.27015)))
        
        # フラクタルタイプ更新
        if self.current_fractal.params.get('is_julia', False):
            self.frac_type_dropdown_var.set("ジュリア集合")
        else:
            self.frac_type_dropdown_var.set("マンデルブロ集合")
        
        # カラーリング更新
        self.coloring_var.set(state['coloring'])
        self.on_coloring_change(None)
        
        # グラデーション更新
        self.gradient_var.set(state['gradient'])
        self.on_gradient_change(None)
        
        # フレーム更新
        self.frames = [frame.copy() for frame in state['frames']]
        self.current_frame_index = state['current_frame_index']
        self.update_frame_tree()
        
        # 再描画
        self.render_fractal()

def main():
    """メイン関数"""
    root = tk.Tk()
    app = FractalGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
