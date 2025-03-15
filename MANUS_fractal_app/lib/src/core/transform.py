"""
ピボット編集とトランスフォーム機能の実装

このモジュールは、Apophysis7x風のピボット編集とトランスフォーム機能を提供します。
"""

import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import math

class Pivot:
    """
    ピボットポイントを表すクラス
    
    ピボットは、フラクタルの変形や操作の中心点として機能します。
    """
    
    def __init__(self, x=0.0, y=0.0, rotation=0.0, scale_x=1.0, scale_y=1.0):
        """
        初期化メソッド
        
        Args:
            x (float): X座標
            y (float): Y座標
            rotation (float): 回転角度（度）
            scale_x (float): X方向のスケール
            scale_y (float): Y方向のスケール
        """
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale_x = scale_x
        self.scale_y = scale_y
    
    def get_transform_matrix(self):
        """
        変換行列を取得するメソッド
        
        Returns:
            numpy.ndarray: 3x3の変換行列
        """
        # 回転角度をラジアンに変換
        rad = math.radians(self.rotation)
        
        # 回転行列
        cos_val = math.cos(rad)
        sin_val = math.sin(rad)
        
        # スケーリングを含む変換行列
        matrix = np.array([
            [self.scale_x * cos_val, -self.scale_y * sin_val, self.x],
            [self.scale_x * sin_val, self.scale_y * cos_val, self.y],
            [0, 0, 1]
        ])
        
        return matrix
    
    def apply_transform(self, points):
        """
        点群に変換を適用するメソッド
        
        Args:
            points (numpy.ndarray): 変換する点群 (Nx2)
            
        Returns:
            numpy.ndarray: 変換された点群 (Nx2)
        """
        # 変換行列を取得
        matrix = self.get_transform_matrix()
        
        # 同次座標に変換 (Nx3)
        homogeneous = np.hstack((points, np.ones((points.shape[0], 1))))
        
        # 変換を適用
        transformed = np.dot(homogeneous, matrix.T)
        
        # 元の座標形式に戻す (Nx2)
        return transformed[:, :2]
    
    def to_dict(self):
        """
        辞書形式に変換するメソッド
        
        Returns:
            dict: ピボットのパラメータを含む辞書
        """
        return {
            'x': self.x,
            'y': self.y,
            'rotation': self.rotation,
            'scale_x': self.scale_x,
            'scale_y': self.scale_y
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        辞書からピボットを作成するクラスメソッド
        
        Args:
            data (dict): ピボットのパラメータを含む辞書
            
        Returns:
            Pivot: 作成されたピボットオブジェクト
        """
        return cls(
            x=data.get('x', 0.0),
            y=data.get('y', 0.0),
            rotation=data.get('rotation', 0.0),
            scale_x=data.get('scale_x', 1.0),
            scale_y=data.get('scale_y', 1.0)
        )


class Transform:
    """
    フラクタル変換を表すクラス
    
    複数の変換を組み合わせて複雑なフラクタルを生成します。
    """
    
    def __init__(self, name="Transform", weight=1.0, color=0, pivot=None, variations=None):
        """
        初期化メソッド
        
        Args:
            name (str): 変換の名前
            weight (float): 変換の重み
            color (int): 色インデックス
            pivot (Pivot, optional): ピボットオブジェクト
            variations (dict, optional): バリエーションとその重みの辞書
        """
        self.name = name
        self.weight = weight
        self.color = color
        self.pivot = pivot or Pivot()
        self.variations = variations or {'linear': 1.0}
    
    def apply(self, points):
        """
        点群に変換を適用するメソッド
        
        Args:
            points (numpy.ndarray): 変換する点群 (Nx2)
            
        Returns:
            numpy.ndarray: 変換された点群 (Nx2)
        """
        # ピボット変換を適用
        transformed = self.pivot.apply_transform(points)
        
        # バリエーションを適用
        result = np.zeros_like(transformed)
        
        for var_name, var_weight in self.variations.items():
            if var_name == 'linear':
                # 線形変換（そのまま）
                var_result = transformed
            elif var_name == 'sinusoidal':
                # サイン変換
                var_result = np.sin(transformed)
            elif var_name == 'spherical':
                # 球面変換
                r2 = np.sum(transformed**2, axis=1, keepdims=True)
                r2[r2 == 0] = 1e-10  # ゼロ除算を防ぐ
                var_result = transformed / r2
            elif var_name == 'swirl':
                # 渦巻き変換
                x, y = transformed[:, 0], transformed[:, 1]
                r2 = x**2 + y**2
                sin_r2 = np.sin(r2)
                cos_r2 = np.cos(r2)
                var_result = np.column_stack((
                    x * sin_r2 - y * cos_r2,
                    x * cos_r2 + y * sin_r2
                ))
            else:
                # 未知のバリエーションは線形として扱う
                var_result = transformed
            
            # 重み付けして結果に加算
            result += var_weight * var_result
        
        return result
    
    def to_dict(self):
        """
        辞書形式に変換するメソッド
        
        Returns:
            dict: 変換のパラメータを含む辞書
        """
        return {
            'name': self.name,
            'weight': self.weight,
            'color': self.color,
            'pivot': self.pivot.to_dict(),
            'variations': self.variations
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        辞書から変換を作成するクラスメソッド
        
        Args:
            data (dict): 変換のパラメータを含む辞書
            
        Returns:
            Transform: 作成された変換オブジェクト
        """
        pivot = Pivot.from_dict(data.get('pivot', {}))
        
        return cls(
            name=data.get('name', 'Transform'),
            weight=data.get('weight', 1.0),
            color=data.get('color', 0),
            pivot=pivot,
            variations=data.get('variations', {'linear': 1.0})
        )


class PivotEditor:
    """
    ピボット編集用のGUIコンポーネント
    """
    
    def __init__(self, canvas, pivot=None, callback=None):
        """
        初期化メソッド
        
        Args:
            canvas (tk.Canvas): 描画用キャンバス
            pivot (Pivot, optional): 編集するピボットオブジェクト
            callback (function, optional): 変更時に呼び出すコールバック関数
        """
        self.canvas = canvas
        self.pivot = pivot or Pivot()
        self.callback = callback
        
        # 表示スケール（キャンバス座標とフラクタル座標の変換用）
        self.scale = 100.0  # 1フラクタル単位 = 100ピクセル
        self.offset_x = self.canvas.winfo_width() / 2
        self.offset_y = self.canvas.winfo_height() / 2
        
        # ドラッグ状態
        self.dragging = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_start_pivot = None
        
        # キャンバスアイテム
        self.pivot_items = {}
        
        # キャンバスイベントをバインド
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # 初期描画
        self.draw_pivot()
    
    def fractal_to_canvas(self, x, y):
        """
        フラクタル座標をキャンバス座標に変換するメソッド
        
        Args:
            x (float): フラクタル座標系のX座標
            y (float): フラクタル座標系のY座標
            
        Returns:
            tuple: キャンバス座標系の(X, Y)
        """
        canvas_x = self.offset_x + x * self.scale
        canvas_y = self.offset_y - y * self.scale  # Y軸は反転
        
        return canvas_x, canvas_y
    
    def canvas_to_fractal(self, canvas_x, canvas_y):
        """
        キャンバス座標をフラクタル座標に変換するメソッド
        
        Args:
            canvas_x (float): キャンバス座標系のX座標
            canvas_y (float): キャンバス座標系のY座標
            
        Returns:
            tuple: フラクタル座標系の(X, Y)
        """
        x = (canvas_x - self.offset_x) / self.scale
        y = (self.offset_y - canvas_y) / self.scale  # Y軸は反転
        
        return x, y
    
    def draw_pivot(self):
        """
        ピボットを描画するメソッド
        """
        # 既存のアイテムを削除
        for item in self.pivot_items.values():
            self.canvas.delete(item)
        
        self.pivot_items = {}
        
        # ピボットの中心点をキャンバス座標に変換
        center_x, center_y = self.fractal_to_canvas(self.pivot.x, self.pivot.y)
        
        # 中心点を描画
        self.pivot_items['center'] = self.canvas.create_oval(
            center_x - 5, center_y - 5,
            center_x + 5, center_y + 5,
            fill="red", outline="white", tags="pivot_center"
        )
        
        # 回転角度をラジアンに変換
        rad = math.radians(self.pivot.rotation)
        
        # X軸方向の線を描画
        x_end_x = center_x + 50 * self.pivot.scale_x * math.cos(rad)
        x_end_y = center_y - 50 * self.pivot.scale_x * math.sin(rad)
        
        self.pivot_items['x_axis'] = self.canvas.create_line(
            center_x, center_y, x_end_x, x_end_y,
            fill="red", width=2, tags="pivot_x_axis"
        )
        
        # X軸の端点を描画
        self.pivot_items['x_handle'] = self.canvas.create_oval(
            x_end_x - 5, x_end_y - 5,
            x_end_x + 5, x_end_y + 5,
            fill="yellow", outline="white", tags="pivot_x_handle"
        )
        
        # Y軸方向の線を描画
        y_end_x = center_x - 50 * self.pivot.scale_y * math.sin(rad)
        y_end_y = center_y - 50 * self.pivot.scale_y * math.cos(rad)
        
        self.pivot_items['y_axis'] = self.canvas.create_line(
            center_x, center_y, y_end_x, y_end_y,
            fill="green", width=2, tags="pivot_y_axis"
        )
        
        # Y軸の端点を描画
        self.pivot_items['y_handle'] = self.canvas.create_oval(
            y_end_x - 5, y_end_y - 5,
            y_end_x + 5, y_end_y + 5,
            fill="cyan", outline="white", tags="pivot_y_handle"
        )
        
        # 回転ハンドルを描画
        rot_radius = 30
        rot_x = center_x + rot_radius * math.cos(rad - math.pi/4)
        rot_y = center_y - rot_radius * math.sin(rad - math.pi/4)
        
        self.pivot_items['rot_handle'] = self.canvas.create_oval(
            rot_x - 5, rot_y - 5,
            rot_x + 5, rot_y + 5,
            fill="magenta", outline="white", tags="pivot_rot_handle"
        )
    
    def on_click(self, event):
        """
        クリック時のイベントハンドラ
        
        Args:
            event: イベントオブジェクト
        """
        # クリックされたアイテムを特定
        item = self.canvas.find_closest(event.x, event.y)
        
        if not item:
            return
        
        tags = self.canvas.gettags(item)
        
        if "pivot_center" in tags:
            self.dragging = "center"
        elif "pivot_x_handle" in tags:
            self.dragging = "x_handle"
        elif "pivot_y_handle" in tags:
            self.dragging = "y_handle"
        elif "pivot_rot_handle" in tags:
            self.dragging = "rot_handle"
        else:
            self.dragging = None
            return
        
        # ドラッグ開始位置を記録
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
        # 現在のピボット状態をコピー
        self.drag_start_pivot = Pivot(
            x=self.pivot.x,
            y=self.pivot.y,
            rotation=self.pivot.rotation,
            scale_x=self.pivot.scale_x,
            scale_y=self.pivot.scale_y
        )
    
    def on_drag(self, event):
        """
        ドラッグ時のイベントハンドラ
        
        Args:
            event: イベントオブジェクト
        """
        if not self.dragging:
            return
        
        # ドラッグ距離を計算
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        # ピボットの中心点をキャンバス座標に変換
        center_x, center_y = self.fractal_to_canvas(self.pivot.x, self.pivot.y)
        
        if self.dragging == "center":
            # 中心点の移動
            new_x, new_y = self.canvas_to_fractal(
                self.drag_start_x + dx,
                self.drag_start_y + dy
            )
            
            self.pivot.x = new_x
            self.pivot.y = new_y
            
        elif self.dragging == "x_handle":
            # X軸のスケールと回転を調整
            # 現在のマウス位置と中心点の角度を計算
            angle = math.atan2(center_y - event.y, event.x - center_x)
            
            # 回転角度を設定（ラジアンから度に変換）
            self.pivot.rotation = math.degrees(angle)
            
            # スケールを計算
            distance = math.sqrt((event.x - center_x)**2 + (event.y - center_y)**2)
            self.pivot.scale_x = distance / 50.0
            
        elif self.dragging == "y_handle":
            # Y軸のスケールを調整
            # 現在の回転角度
            rad = math.radians(self.pivot.rotation)
            
            # Y軸方向のベクトル
            y_dir_x = -math.sin(rad)
            y_dir_y = -math.cos(rad)
            
            # マウス位置と中心点の差分
            mouse_dx = event.x - center_x
            mouse_dy = event.y - center_y
            
            # Y軸方向への投影
            projection = mouse_dx * y_dir_x + mouse_dy * y_dir_y
            
            # スケールを計算
            self.pivot.scale_y = abs(projection) / 50.0
            
            # 符号を調整
            if projection < 0:
                self.pivot.scale_y = -self.pivot.scale_y
            
        elif self.dragging == "rot_handle":
            # 回転のみを調整
            # 現在のマウス位置と中心点の角度を計算
            angle = math.atan2(center_y - event.y, event.x - center_x)
            
            # 回転角度を設定（ラジアンから度に変換）
            self.pivot.rotation = math.degrees(angle) + 45  # 45度オフセット
        
        # ピボットを再描画
        self.draw_pivot()
        
        # コールバックを呼び出す
        if self.callback:
            self.callback(self.pivot)
    
    def on_release(self, event):
        """
        マウスリリース時のイベントハンドラ
        
        Args:
            event: イベントオブジェクト
        """
        self.dragging = None
    
    def set_pivot(self, pivot):
        """
        ピボットを設定するメソッド
        
        Args:
            pivot (Pivot): 設定するピボットオブジェクト
        """
        self.pivot = pivot
        self.draw_pivot()
    
    def get_pivot(self):
        """
        現在のピボットを取得するメソッド
        
        Returns:
            Pivot: 現在のピボットオブジェクト
        """
        return self.pivot


class TransformEditor:
    """
    変換編集用のGUIコンポーネント
    """
    
    def __init__(self, parent, transform=None, callback=None):
        """
        初期化メソッド
        
        Args:
            parent (tk.Frame): 親ウィジェット
            transform (Transform, optional): 編集する変換オブジェクト
            callback (function, optional): 変更時に呼び出すコールバック関数
        """
        self.parent = parent
        self.transform = transform or Transform()
        self.callback = callback
        
        # UIコンポーネントを作成
        self.create_widgets()
    
    def create_widgets(self):
        """
        UIコンポーネントを作成するメソッド
        """
        # メインフレーム
        self.frame = tk.Frame(self.parent, bg="darkgray", padx=5, pady=5)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # 変換名
        name_frame = tk.Frame(self.frame, bg="lightblue")
        name_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(name_frame, text="名前:", bg="lightblue").pack(side=tk.LEFT)
        
        self.name_var = tk.StringVar(value=self.transform.name)
        name_entry = tk.Entry(name_frame, textvariable=self.name_var)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        name_entry.bind("<KeyRelease>", self.on_param_change)
        
        # 重み
        weight_frame = tk.Frame(self.frame, bg="lightblue")
        weight_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(weight_frame, text="重み:", bg="lightblue").pack(side=tk.LEFT)
        
        self.weight_var = tk.StringVar(value=str(self.transform.weight))
        weight_entry = tk.Entry(weight_frame, textvariable=self.weight_var)
        weight_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        weight_entry.bind("<KeyRelease>", self.on_param_change)
        
        # 色インデックス
        color_frame = tk.Frame(self.frame, bg="lightblue")
        color_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(color_frame, text="色:", bg="lightblue").pack(side=tk.LEFT)
        
        self.color_var = tk.StringVar(value=str(self.transform.color))
        color_entry = tk.Entry(color_frame, textvariable=self.color_var)
        color_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        color_entry.bind("<KeyRelease>", self.on_param_change)
        
        # ピボット編集用キャンバス
        canvas_frame = tk.Frame(self.frame, bg="black")
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        
        self.canvas = tk.Canvas(canvas_frame, bg="black", width=300, height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # ピボットエディタを作成
        self.pivot_editor = PivotEditor(self.canvas, self.transform.pivot, self.on_pivot_change)
        
        # バリエーション編集
        var_frame = tk.Frame(self.frame, bg="lightblue")
        var_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(var_frame, text="バリエーション:", bg="lightblue").pack(anchor=tk.W)
        
        # バリエーションリスト
        self.var_listbox = tk.Listbox(var_frame, height=5)
        self.var_listbox.pack(fill=tk.X, expand=True)
        
        # バリエーションを追加
        for var_name, var_weight in self.transform.variations.items():
            self.var_listbox.insert(tk.END, f"{var_name}: {var_weight}")
        
        # バリエーション編集ボタン
        var_button_frame = tk.Frame(var_frame, bg="lightblue")
        var_button_frame.pack(fill=tk.X)
        
        add_var_button = tk.Button(var_button_frame, text="追加", command=self.add_variation)
        add_var_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        edit_var_button = tk.Button(var_button_frame, text="編集", command=self.edit_variation)
        edit_var_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        remove_var_button = tk.Button(var_button_frame, text="削除", command=self.remove_variation)
        remove_var_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def on_param_change(self, event=None):
        """
        パラメータ変更時のイベントハンドラ
        
        Args:
            event: イベントオブジェクト
        """
        try:
            # 変換名を更新
            self.transform.name = self.name_var.get()
            
            # 重みを更新
            weight = float(self.weight_var.get())
            if weight >= 0:
                self.transform.weight = weight
            
            # 色インデックスを更新
            color = int(self.color_var.get())
            if color >= 0:
                self.transform.color = color
            
            # コールバックを呼び出す
            if self.callback:
                self.callback(self.transform)
                
        except ValueError:
            # 数値変換エラーは無視
            pass
    
    def on_pivot_change(self, pivot):
        """
        ピボット変更時のコールバック
        
        Args:
            pivot (Pivot): 変更されたピボットオブジェクト
        """
        self.transform.pivot = pivot
        
        # コールバックを呼び出す
        if self.callback:
            self.callback(self.transform)
    
    def add_variation(self):
        """
        バリエーションを追加するメソッド
        """
        # バリエーション追加ダイアログ
        dialog = tk.Toplevel(self.parent)
        dialog.title("バリエーション追加")
        dialog.geometry("300x150")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        tk.Label(dialog, text="バリエーション名:").pack(anchor=tk.W, padx=5, pady=5)
        
        var_name_var = tk.StringVar(value="linear")
        var_name_combo = ttk.Combobox(dialog, textvariable=var_name_var)
        var_name_combo['values'] = ["linear", "sinusoidal", "spherical", "swirl", "horseshoe", "polar", "handkerchief", "heart"]
        var_name_combo.pack(fill=tk.X, padx=5)
        
        tk.Label(dialog, text="重み:").pack(anchor=tk.W, padx=5, pady=5)
        
        var_weight_var = tk.StringVar(value="1.0")
        var_weight_entry = tk.Entry(dialog, textvariable=var_weight_var)
        var_weight_entry.pack(fill=tk.X, padx=5)
        
        def on_ok():
            try:
                var_name = var_name_var.get()
                var_weight = float(var_weight_var.get())
                
                # バリエーションを追加
                self.transform.variations[var_name] = var_weight
                
                # リストボックスを更新
                self.var_listbox.delete(0, tk.END)
                for name, weight in self.transform.variations.items():
                    self.var_listbox.insert(tk.END, f"{name}: {weight}")
                
                # コールバックを呼び出す
                if self.callback:
                    self.callback(self.transform)
                
                dialog.destroy()
                
            except ValueError:
                tk.messagebox.showerror("エラー", "重みは数値で入力してください")
        
        ok_button = tk.Button(dialog, text="OK", command=on_ok)
        ok_button.pack(pady=10)
    
    def edit_variation(self):
        """
        選択されたバリエーションを編集するメソッド
        """
        # 選択されたアイテム
        selection = self.var_listbox.curselection()
        if not selection:
            return
        
        # 選択されたバリエーション
        var_str = self.var_listbox.get(selection[0])
        var_name, var_weight_str = var_str.split(": ")
        
        # バリエーション編集ダイアログ
        dialog = tk.Toplevel(self.parent)
        dialog.title("バリエーション編集")
        dialog.geometry("300x100")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"バリエーション: {var_name}").pack(anchor=tk.W, padx=5, pady=5)
        
        tk.Label(dialog, text="重み:").pack(anchor=tk.W, padx=5)
        
        var_weight_var = tk.StringVar(value=var_weight_str)
        var_weight_entry = tk.Entry(dialog, textvariable=var_weight_var)
        var_weight_entry.pack(fill=tk.X, padx=5)
        
        def on_ok():
            try:
                var_weight = float(var_weight_var.get())
                
                # バリエーションを更新
                self.transform.variations[var_name] = var_weight
                
                # リストボックスを更新
                self.var_listbox.delete(0, tk.END)
                for name, weight in self.transform.variations.items():
                    self.var_listbox.insert(tk.END, f"{name}: {weight}")
                
                # コールバックを呼び出す
                if self.callback:
                    self.callback(self.transform)
                
                dialog.destroy()
                
            except ValueError:
                tk.messagebox.showerror("エラー", "重みは数値で入力してください")
        
        ok_button = tk.Button(dialog, text="OK", command=on_ok)
        ok_button.pack(pady=10)
    
    def remove_variation(self):
        """
        選択されたバリエーションを削除するメソッド
        """
        # 選択されたアイテム
        selection = self.var_listbox.curselection()
        if not selection:
            return
        
        # 選択されたバリエーション
        var_str = self.var_listbox.get(selection[0])
        var_name, _ = var_str.split(": ")
        
        # 最後のバリエーションは削除できない
        if len(self.transform.variations) <= 1:
            tk.messagebox.showwarning("警告", "少なくとも1つのバリエーションが必要です")
            return
        
        # バリエーションを削除
        del self.transform.variations[var_name]
        
        # リストボックスを更新
        self.var_listbox.delete(0, tk.END)
        for name, weight in self.transform.variations.items():
            self.var_listbox.insert(tk.END, f"{name}: {weight}")
        
        # コールバックを呼び出す
        if self.callback:
            self.callback(self.transform)
    
    def set_transform(self, transform):
        """
        変換を設定するメソッド
        
        Args:
            transform (Transform): 設定する変換オブジェクト
        """
        self.transform = transform
        
        # UIを更新
        self.name_var.set(transform.name)
        self.weight_var.set(str(transform.weight))
        self.color_var.set(str(transform.color))
        
        # ピボットエディタを更新
        self.pivot_editor.set_pivot(transform.pivot)
        
        # バリエーションリストを更新
        self.var_listbox.delete(0, tk.END)
        for var_name, var_weight in transform.variations.items():
            self.var_listbox.insert(tk.END, f"{var_name}: {weight}")
    
    def get_transform(self):
        """
        現在の変換を取得するメソッド
        
        Returns:
            Transform: 現在の変換オブジェクト
        """
        return self.transform
