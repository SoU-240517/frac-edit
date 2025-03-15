"""
マンデルブロ集合とジュリア集合の実装

このモジュールは、マンデルブロ集合とジュリア集合を計算するクラスを提供します。
"""

import numpy as np
from .fractal_base import FractalBase

class MandelbrotJulia(FractalBase):
    """
    マンデルブロ集合とジュリア集合を計算するクラス
    
    z_{n+1} = z_n^2 + c という漸化式に基づいて計算します。
    マンデルブロ集合の場合は、c = 座標点、z_0 = 0
    ジュリア集合の場合は、c = 定数、z_0 = 座標点
    """
    
    def __init__(self, width, height):
        """
        初期化メソッド
        
        Args:
            width (int): 画像の幅（ピクセル数）
            height (int): 画像の高さ（ピクセル数）
        """
        super().__init__(width, height)
        
        # デフォルトパラメータ
        self.params = {
            'max_iter': 100,      # 最大反復回数
            'escape_radius': 2.0, # 発散と判定する半径
            'c_real': -0.7,       # cの実部（ジュリア集合用）
            'c_imag': 0.27015,    # cの虚部（ジュリア集合用）
            'z_real': 0.0,        # zの初期値の実部（マンデルブロ集合用）
            'z_imag': 0.0,        # zの初期値の虚部（マンデルブロ集合用）
            'is_julia': False     # True=ジュリア集合、False=マンデルブロ集合
        }
    
    def calculate(self, x_min, x_max, y_min, y_max):
        """
        フラクタルを計算するメソッド
        
        Args:
            x_min (float): X座標の最小値
            x_max (float): X座標の最大値
            y_min (float): Y座標の最小値
            y_max (float): Y座標の最大値
            
        Returns:
            numpy.ndarray: 計算結果の2次元配列（各要素は発散するまでの反復回数）
        """
        # 座標グリッドを作成
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_min, y_max, self.height)
        X, Y = np.meshgrid(x, y)
        
        # 複素数グリッドを作成
        C = X + 1j * Y
        
        # 結果を格納する配列
        result = np.zeros((self.height, self.width), dtype=np.int32)
        
        # パラメータを取得
        max_iter = self.params['max_iter']
        escape_radius = self.params['escape_radius']
        is_julia = self.params['is_julia']
        
        if is_julia:
            # ジュリア集合の場合
            c = complex(self.params['c_real'], self.params['c_imag'])
            Z = C.copy()  # 初期値はグリッド上の点
        else:
            # マンデルブロ集合の場合
            z0 = complex(self.params['z_real'], self.params['z_imag'])
            Z = np.full(C.shape, z0)  # 初期値は固定
            c = C  # パラメータはグリッド上の点
        
        # 反復計算
        for i in range(max_iter):
            # 発散していない点のマスク
            mask = np.abs(Z) < escape_radius
            
            # 発散していない点のみ計算を続ける
            Z[mask] = Z[mask]**2 + c[mask]
            
            # 今回の反復で発散した点を記録
            result[(mask & (np.abs(Z) >= escape_radius))] = i + 1
        
        return result
    
    def get_params(self):
        """
        パラメータ情報を取得するメソッド
        
        Returns:
            dict: パラメータ名と設定値の辞書
        """
        return self.params.copy()
    
    def set_params(self, params):
        """
        パラメータを設定するメソッド
        
        Args:
            params (dict): パラメータ名と設定値の辞書
        """
        for key, value in params.items():
            if key in self.params:
                self.params[key] = value
