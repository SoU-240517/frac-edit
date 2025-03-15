"""
フラクタルジェネレータの基本クラス

このモジュールは、フラクタル計算の基本となる抽象クラスを提供します。
すべてのフラクタルタイプはこのクラスを継承して実装します。
"""

import numpy as np
from abc import ABC, abstractmethod

class FractalBase(ABC):
    """
    フラクタル計算の基本クラス
    
    すべてのフラクタルタイプはこのクラスを継承して実装します。
    """
    
    def __init__(self, width, height):
        """
        初期化メソッド
        
        Args:
            width (int): 画像の幅（ピクセル数）
            height (int): 画像の高さ（ピクセル数）
        """
        self.width = width
        self.height = height
        self.params = {}  # パラメータを保存する辞書
        
    @abstractmethod
    def calculate(self, x_min, x_max, y_min, y_max):
        """
        フラクタルを計算するメソッド（サブクラスで実装必須）
        
        Args:
            x_min (float): X座標の最小値
            x_max (float): X座標の最大値
            y_min (float): Y座標の最小値
            y_max (float): Y座標の最大値
            
        Returns:
            numpy.ndarray: 計算結果の2次元配列
        """
        pass
    
    @abstractmethod
    def get_params(self):
        """
        パラメータ情報を取得するメソッド（サブクラスで実装必須）
        
        Returns:
            dict: パラメータ名と設定値の辞書
        """
        pass
    
    @abstractmethod
    def set_params(self, params):
        """
        パラメータを設定するメソッド（サブクラスで実装必須）
        
        Args:
            params (dict): パラメータ名と設定値の辞書
        """
        pass
    
    def resize(self, width, height):
        """
        画像サイズを変更するメソッド
        
        Args:
            width (int): 新しい幅（ピクセル数）
            height (int): 新しい高さ（ピクセル数）
        """
        self.width = width
        self.height = height
