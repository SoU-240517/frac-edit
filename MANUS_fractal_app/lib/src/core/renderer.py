"""
フラクタル描画エンジン

このモジュールは、フラクタル計算結果を画像として描画する機能を提供します。
"""

import numpy as np
from PIL import Image
import threading
import multiprocessing

class FractalRenderer:
    """
    フラクタル描画エンジン
    
    フラクタル計算結果を画像として描画します。
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
        self.background_color = (0, 0, 0, 255)  # 背景色（RGBA）
        
    def render(self, fractal, x_min, x_max, y_min, y_max, coloring_algorithm, gradient):
        """
        フラクタルを描画するメソッド
        
        Args:
            fractal (FractalBase): フラクタルオブジェクト
            x_min (float): X座標の最小値
            x_max (float): X座標の最大値
            y_min (float): Y座標の最小値
            y_max (float): Y座標の最大値
            coloring_algorithm (ColoringAlgorithm): カラーリングアルゴリズム
            gradient (list): カラーグラデーション（RGBAタプルのリスト）
            
        Returns:
            PIL.Image: 描画された画像
        """
        # フラクタルを計算
        fractal_data = fractal.calculate(x_min, x_max, y_min, y_max)
        
        # カラーリングを適用
        colored_data = coloring_algorithm.apply(fractal_data, gradient)
        
        # PILイメージに変換
        image = Image.fromarray(colored_data, mode='RGBA')
        
        return image
    
    def render_high_quality(self, fractal, x_min, x_max, y_min, y_max, coloring_algorithm, gradient, 
                           oversample=2, filter_radius=0.5, quality=100):
        """
        高品質なフラクタル描画を行うメソッド
        
        Args:
            fractal (FractalBase): フラクタルオブジェクト
            x_min (float): X座標の最小値
            x_max (float): X座標の最大値
            y_min (float): Y座標の最小値
            y_max (float): Y座標の最大値
            coloring_algorithm (ColoringAlgorithm): カラーリングアルゴリズム
            gradient (list): カラーグラデーション（RGBAタプルのリスト）
            oversample (int): オーバーサンプリングの倍率
            filter_radius (float): フィルターの半径
            quality (int): 品質レベル（1～100）
            
        Returns:
            PIL.Image: 描画された高品質画像
        """
        # オーバーサンプリングのために一時的に解像度を上げる
        original_width = fractal.width
        original_height = fractal.height
        
        # 一時的に解像度を上げる
        fractal.resize(self.width * oversample, self.height * oversample)
        
        # 高解像度で計算
        fractal_data = fractal.calculate(x_min, x_max, y_min, y_max)
        
        # カラーリングを適用
        colored_data = coloring_algorithm.apply(fractal_data, gradient)
        
        # 高解像度画像を作成
        high_res_image = Image.fromarray(colored_data, mode='RGBA')
        
        # 元の解像度にリサイズ（高品質なフィルタリングを適用）
        image = high_res_image.resize((self.width, self.height), Image.LANCZOS)
        
        # 元の解像度に戻す
        fractal.resize(original_width, original_height)
        
        return image
    
    def render_parallel(self, fractal, x_min, x_max, y_min, y_max, coloring_algorithm, gradient, num_threads=None):
        """
        並列処理でフラクタルを描画するメソッド
        
        Args:
            fractal (FractalBase): フラクタルオブジェクト
            x_min (float): X座標の最小値
            x_max (float): X座標の最大値
            y_min (float): Y座標の最小値
            y_max (float): Y座標の最大値
            coloring_algorithm (ColoringAlgorithm): カラーリングアルゴリズム
            gradient (list): カラーグラデーション（RGBAタプルのリスト）
            num_threads (int, optional): 使用するスレッド数（Noneの場合はCPUコア数）
            
        Returns:
            PIL.Image: 描画された画像
        """
        # スレッド数を決定
        if num_threads is None:
            num_threads = multiprocessing.cpu_count()
        
        # 画像を分割して計算
        height_per_thread = self.height // num_threads
        
        # 結果を格納する配列
        result = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        
        # スレッドのリスト
        threads = []
        
        # 各スレッドで計算する関数
        def calculate_segment(start_y, end_y, segment_index):
            # Y座標の範囲を計算
            segment_y_min = y_min + (y_max - y_min) * (start_y / self.height)
            segment_y_max = y_min + (y_max - y_min) * (end_y / self.height)
            
            # フラクタルを計算
            segment_fractal = type(fractal)(self.width, end_y - start_y)
            segment_fractal.set_params(fractal.get_params())
            segment_data = segment_fractal.calculate(x_min, x_max, segment_y_min, segment_y_max)
            
            # カラーリングを適用
            segment_colored = coloring_algorithm.apply(segment_data, gradient)
            
            # 結果を格納
            result[start_y:end_y, :, :] = segment_colored
        
        # スレッドを作成して開始
        for i in range(num_threads):
            start_y = i * height_per_thread
            end_y = start_y + height_per_thread if i < num_threads - 1 else self.height
            
            thread = threading.Thread(
                target=calculate_segment,
                args=(start_y, end_y, i)
            )
            threads.append(thread)
            thread.start()
        
        # すべてのスレッドが終了するのを待つ
        for thread in threads:
            thread.join()
        
        # PILイメージに変換
        image = Image.fromarray(result, mode='RGBA')
        
        return image
    
    def set_background_color(self, color):
        """
        背景色を設定するメソッド
        
        Args:
            color (tuple): RGBA形式の色（例: (255, 0, 0, 255)）
        """
        self.background_color = color
    
    def apply_background_gradient(self, image, gradient_colors):
        """
        背景にグラデーションを適用するメソッド
        
        Args:
            image (PIL.Image): 元の画像
            gradient_colors (list): グラデーションの色ポイントのリスト [(位置, (R, G, B, A)), ...]
            
        Returns:
            PIL.Image: 背景グラデーションが適用された画像
        """
        # 背景画像を作成
        background = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        
        # 背景にグラデーションを描画
        from PIL import ImageDraw
        draw = ImageDraw.Draw(background)
        
        # 単純な線形グラデーション（上から下）
        for y in range(self.height):
            # 位置（0.0～1.0）
            pos = y / (self.height - 1)
            
            # 位置に対応する色を見つける
            color = None
            for i in range(len(gradient_colors) - 1):
                pos1, color1 = gradient_colors[i]
                pos2, color2 = gradient_colors[i + 1]
                
                if pos1 <= pos <= pos2:
                    # 2つの色の間を線形補間
                    t = (pos - pos1) / (pos2 - pos1) if pos2 > pos1 else 0
                    r = int(color1[0] * (1 - t) + color2[0] * t)
                    g = int(color1[1] * (1 - t) + color2[1] * t)
                    b = int(color1[2] * (1 - t) + color2[2] * t)
                    a = int(color1[3] * (1 - t) + color2[3] * t)
                    color = (r, g, b, a)
                    break
            
            if color is None:
                # 範囲外の場合は最も近い端の色を使用
                if pos < gradient_colors[0][0]:
                    color = gradient_colors[0][1]
                else:
                    color = gradient_colors[-1][1]
            
            # 水平線を描画
            draw.line([(0, y), (self.width, y)], fill=color)
        
        # 元の画像と背景を合成
        result = Image.alpha_composite(background, image)
        
        return result
    
    def apply_effects(self, image, effects=None):
        """
        画像にエフェクトを適用するメソッド
        
        Args:
            image (PIL.Image): 元の画像
            effects (dict, optional): 適用するエフェクトの辞書
            
        Returns:
            PIL.Image: エフェクトが適用された画像
        """
        if effects is None:
            return image
        
        result = image.copy()
        
        # ドロップシャドウ
        if 'drop_shadow' in effects:
            from PIL import ImageFilter
            
            shadow_params = effects['drop_shadow']
            offset_x = shadow_params.get('offset_x', 5)
            offset_y = shadow_params.get('offset_y', 5)
            blur_radius = shadow_params.get('blur_radius', 3)
            shadow_color = shadow_params.get('color', (0, 0, 0, 128))
            
            # 影用の画像を作成
            shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
            shadow_mask = image.split()[3]  # アルファチャンネルを取得
            shadow.putalpha(shadow_mask)
            
            # 影をぼかす
            shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
            
            # 影の色を設定
            shadow_data = np.array(shadow)
            shadow_data[..., 0] = shadow_color[0]
            shadow_data[..., 1] = shadow_color[1]
            shadow_data[..., 2] = shadow_color[2]
            shadow_data[..., 3] = (shadow_data[..., 3] * shadow_color[3] // 255)
            shadow = Image.fromarray(shadow_data)
            
            # 新しい画像を作成して影を配置
            combined = Image.new('RGBA', image.size, (0, 0, 0, 0))
            combined.paste(shadow, (offset_x, offset_y))
            combined.paste(image, (0, 0), image)
            
            result = combined
        
        # 光彩（外側）
        if 'outer_glow' in effects:
            from PIL import ImageFilter
            
            glow_params = effects['outer_glow']
            blur_radius = glow_params.get('blur_radius', 5)
            glow_color = glow_params.get('color', (255, 255, 255, 128))
            
            # 光彩用の画像を作成
            glow = Image.new('RGBA', image.size, (0, 0, 0, 0))
            glow_mask = image.split()[3]  # アルファチャンネルを取得
            glow.putalpha(glow_mask)
            
            # 光彩をぼかす
            glow = glow.filter(ImageFilter.GaussianBlur(blur_radius))
            
            # 光彩の色を設定
            glow_data = np.array(glow)
            glow_data[..., 0] = glow_color[0]
            glow_data[..., 1] = glow_color[1]
            glow_data[..., 2] = glow_color[2]
            glow_data[..., 3] = (glow_data[..., 3] * glow_color[3] // 255)
            glow = Image.fromarray(glow_data)
            
            # 新しい画像を作成して光彩と元の画像を合成
            combined = Image.new('RGBA', image.size, (0, 0, 0, 0))
            combined.paste(glow, (0, 0))
            combined.paste(image, (0, 0), image)
            
            result = combined
        
        # 透明度
        if 'transparency' in effects:
            transparency = effects['transparency']
            alpha_factor = 1.0 - (transparency / 100.0)
            
            # 透明度を適用
            result_data = np.array(result)
            result_data[..., 3] = (result_data[..., 3] * alpha_factor).astype(np.uint8)
            result = Image.fromarray(result_data)
        
        return result
