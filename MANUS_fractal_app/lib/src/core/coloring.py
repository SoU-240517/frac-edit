"""
カラーリングアルゴリズムの実装

このモジュールは、フラクタル計算結果に色を付けるためのアルゴリズムを提供します。
"""

import numpy as np
from abc import ABC, abstractmethod

class ColoringAlgorithm(ABC):
    """
    カラーリングアルゴリズムの基本クラス
    
    すべてのカラーリングアルゴリズムはこのクラスを継承して実装します。
    """
    
    def __init__(self):
        """
        初期化メソッド
        """
        self.params = {}  # パラメータを保存する辞書
    
    @abstractmethod
    def apply(self, fractal_data, gradient):
        """
        カラーリングを適用するメソッド（サブクラスで実装必須）
        
        Args:
            fractal_data (numpy.ndarray): フラクタル計算結果の2次元配列
            gradient (list): カラーグラデーション（RGBAタプルのリスト）
            
        Returns:
            numpy.ndarray: RGBA形式の色付けされた画像データ
        """
        pass
    
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


class IterationColoring(ColoringAlgorithm):
    """
    反復回数に基づくカラーリングアルゴリズム
    
    発散するまでの反復回数に基づいて色を割り当てます。
    """
    
    def __init__(self):
        """
        初期化メソッド
        """
        super().__init__()
        self.params = {
            'cyclic': True,       # 循環的なカラーマッピングを使用するか
            'offset': 0,          # カラーオフセット
            'scale': 1.0,         # カラースケール
            'invert': False,      # 色を反転するか
        }
    
    def apply(self, fractal_data, gradient):
        """
        カラーリングを適用するメソッド
        
        Args:
            fractal_data (numpy.ndarray): フラクタル計算結果の2次元配列
            gradient (list): カラーグラデーション（RGBAタプルのリスト）
            
        Returns:
            numpy.ndarray: RGBA形式の色付けされた画像データ
        """
        height, width = fractal_data.shape
        max_iter = np.max(fractal_data)
        
        # パラメータを取得
        cyclic = self.params['cyclic']
        offset = self.params['offset']
        scale = self.params['scale']
        invert = self.params['invert']
        
        # グラデーションの長さ
        gradient_length = len(gradient)
        
        # 結果を格納する配列（RGBA形式）
        result = np.zeros((height, width, 4), dtype=np.uint8)
        
        # 発散しない点（fractal_data == 0）は黒色にする
        non_divergent = (fractal_data == 0)
        result[non_divergent] = [0, 0, 0, 255]  # 黒色（不透明）
        
        # 発散する点に色を割り当てる
        divergent = ~non_divergent
        
        if divergent.any():
            # 反復回数を正規化（0.0～1.0の範囲に）
            normalized = fractal_data[divergent].astype(float) / max_iter
            
            # スケールとオフセットを適用
            normalized = normalized * scale + offset
            
            if invert:
                normalized = 1.0 - normalized
            
            if cyclic:
                # 循環的なマッピング（0.0～1.0の範囲を繰り返す）
                normalized = normalized % 1.0
            else:
                # 非循環的なマッピング（0.0～1.0の範囲に制限）
                normalized = np.clip(normalized, 0.0, 1.0)
            
            # グラデーションインデックスに変換
            indices = (normalized * (gradient_length - 1)).astype(int)
            
            # 色を割り当て
            for i, idx in enumerate(indices):
                result[divergent][i] = gradient[idx]
        
        return result


class ContinuousPotentialColoring(ColoringAlgorithm):
    """
    連続的ポテンシャル法によるカラーリングアルゴリズム
    
    発散する点のポテンシャルを連続的に計算し、滑らかな色変化を実現します。
    """
    
    def __init__(self):
        """
        初期化メソッド
        """
        super().__init__()
        self.params = {
            'cyclic': True,       # 循環的なカラーマッピングを使用するか
            'offset': 0,          # カラーオフセット
            'scale': 1.0,         # カラースケール
            'invert': False,      # 色を反転するか
            'log_scale': True,    # 対数スケールを使用するか
        }
    
    def apply(self, fractal_data, gradient, z_values=None):
        """
        カラーリングを適用するメソッド
        
        Args:
            fractal_data (numpy.ndarray): フラクタル計算結果の2次元配列
            gradient (list): カラーグラデーション（RGBAタプルのリスト）
            z_values (numpy.ndarray, optional): 最終的なz値の配列（連続的ポテンシャル計算用）
            
        Returns:
            numpy.ndarray: RGBA形式の色付けされた画像データ
        """
        height, width = fractal_data.shape
        
        # パラメータを取得
        cyclic = self.params['cyclic']
        offset = self.params['offset']
        scale = self.params['scale']
        invert = self.params['invert']
        log_scale = self.params['log_scale']
        
        # グラデーションの長さ
        gradient_length = len(gradient)
        
        # 結果を格納する配列（RGBA形式）
        result = np.zeros((height, width, 4), dtype=np.uint8)
        
        # 発散しない点（fractal_data == 0）は黒色にする
        non_divergent = (fractal_data == 0)
        result[non_divergent] = [0, 0, 0, 255]  # 黒色（不透明）
        
        # 発散する点に色を割り当てる
        divergent = ~non_divergent
        
        if divergent.any() and z_values is not None:
            # 連続的ポテンシャルを計算
            # log(log(|z|)) / log(2) を使用
            z_abs = np.abs(z_values[divergent])
            
            if log_scale:
                # 対数スケール
                potential = np.log(np.log(z_abs + 1e-10) + 1e-10) / np.log(2.0)
            else:
                # 線形スケール
                potential = z_abs
            
            # 反復回数と連続的ポテンシャルを組み合わせる
            normalized = fractal_data[divergent].astype(float) - potential
            
            # 正規化（0.0～1.0の範囲に）
            min_val = np.min(normalized)
            max_val = np.max(normalized)
            if max_val > min_val:
                normalized = (normalized - min_val) / (max_val - min_val)
            else:
                normalized = np.zeros_like(normalized)
            
            # スケールとオフセットを適用
            normalized = normalized * scale + offset
            
            if invert:
                normalized = 1.0 - normalized
            
            if cyclic:
                # 循環的なマッピング（0.0～1.0の範囲を繰り返す）
                normalized = normalized % 1.0
            else:
                # 非循環的なマッピング（0.0～1.0の範囲に制限）
                normalized = np.clip(normalized, 0.0, 1.0)
            
            # グラデーションインデックスに変換
            indices = (normalized * (gradient_length - 1)).astype(int)
            
            # 色を割り当て
            for i, idx in enumerate(indices):
                result[divergent][i] = gradient[idx]
        else:
            # z_valuesがない場合は通常の反復回数カラーリングを使用
            iter_coloring = IterationColoring()
            iter_coloring.set_params(self.params)
            result = iter_coloring.apply(fractal_data, gradient)
        
        return result


class GradientGenerator:
    """
    カラーグラデーションを生成するクラス
    """
    
    @staticmethod
    def create_rgb_gradient(colors, num_points=256):
        """
        RGBカラーグラデーションを生成します
        
        Args:
            colors (list): カラーポイントのリスト [(位置, (R, G, B, A)), ...]
                           位置は0.0～1.0の範囲
            num_points (int): グラデーションの分割数
            
        Returns:
            list: RGBAタプルのリスト
        """
        # 位置でソート
        sorted_colors = sorted(colors, key=lambda x: x[0])
        
        # 結果を格納するリスト
        gradient = []
        
        # グラデーションを生成
        for i in range(num_points):
            # 現在の位置（0.0～1.0）
            pos = i / (num_points - 1)
            
            # 位置に対応する色を見つける
            for j in range(len(sorted_colors) - 1):
                pos1, color1 = sorted_colors[j]
                pos2, color2 = sorted_colors[j + 1]
                
                if pos1 <= pos <= pos2:
                    # 2つの色の間を線形補間
                    t = (pos - pos1) / (pos2 - pos1) if pos2 > pos1 else 0
                    r = int(color1[0] * (1 - t) + color2[0] * t)
                    g = int(color1[1] * (1 - t) + color2[1] * t)
                    b = int(color1[2] * (1 - t) + color2[2] * t)
                    a = int(color1[3] * (1 - t) + color2[3] * t)
                    gradient.append((r, g, b, a))
                    break
            else:
                # 範囲外の場合は最も近い端の色を使用
                if pos < sorted_colors[0][0]:
                    gradient.append(sorted_colors[0][1])
                else:
                    gradient.append(sorted_colors[-1][1])
        
        return gradient
    
    @staticmethod
    def create_preset_gradients():
        """
        プリセットグラデーションを生成します
        
        Returns:
            dict: グラデーション名とグラデーションのマッピング
        """
        presets = {}
        
        # 虹色グラデーション
        rainbow = [
            (0.0, (255, 0, 0, 255)),      # 赤
            (0.2, (255, 165, 0, 255)),    # オレンジ
            (0.4, (255, 255, 0, 255)),    # 黄
            (0.6, (0, 255, 0, 255)),      # 緑
            (0.8, (0, 0, 255, 255)),      # 青
            (1.0, (128, 0, 128, 255))     # 紫
        ]
        presets['rainbow'] = GradientGenerator.create_rgb_gradient(rainbow)
        
        # 熱色グラデーション
        hot = [
            (0.0, (0, 0, 0, 255)),        # 黒
            (0.3, (128, 0, 0, 255)),      # 暗い赤
            (0.6, (255, 0, 0, 255)),      # 赤
            (0.8, (255, 255, 0, 255)),    # 黄
            (1.0, (255, 255, 255, 255))   # 白
        ]
        presets['hot'] = GradientGenerator.create_rgb_gradient(hot)
        
        # 寒色グラデーション
        cool = [
            (0.0, (0, 0, 128, 255)),      # 暗い青
            (0.5, (0, 128, 255, 255)),    # 水色
            (1.0, (255, 255, 255, 255))   # 白
        ]
        presets['cool'] = GradientGenerator.create_rgb_gradient(cool)
        
        # モノクロームグラデーション
        monochrome = [
            (0.0, (0, 0, 0, 255)),        # 黒
            (1.0, (255, 255, 255, 255))   # 白
        ]
        presets['monochrome'] = GradientGenerator.create_rgb_gradient(monochrome)
        
        # 宇宙風グラデーション
        cosmic = [
            (0.0, (0, 0, 0, 255)),        # 黒
            (0.3, (75, 0, 130, 255)),     # インディゴ
            (0.6, (148, 0, 211, 255)),    # バイオレット
            (0.8, (255, 105, 180, 255)),  # ホットピンク
            (1.0, (255, 255, 255, 255))   # 白
        ]
        presets['cosmic'] = GradientGenerator.create_rgb_gradient(cosmic)
        
        return presets
