# julia_viewer/core/color_map.py
import numpy as np
from tkinter import colorchooser

def hex_to_rgb(hex_color):
    """16進数カラーコードをRGB値に変換"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def is_valid_hex_color(color):
    """16進数カラーコードの形式を検証"""
    if not color.startswith('#'):
        return False
    try:
        int(color[1:], 16)
        return len(color) == 7
    except ValueError:
        return False

def create_colormap(values, start_color_hex, end_color_hex):
    """カラーマップを作成する関数"""
    # 開始色と終了色のRGB値を取得
    try:
        start_rgb = hex_to_rgb(start_color_hex)
        end_rgb = hex_to_rgb(end_color_hex)
    except:
        # エラーの場合はデフォルトの色を使用
        start_rgb = (0, 0, 255)
        end_rgb = (255, 255, 255)

    colors = np.zeros((values.shape[0], values.shape[1], 3), dtype=np.uint8)

    # 値を0-1に正規化
    normalized = np.where(values > 0, values, 0)

    # 各色成分に対してグラデーションを計算
    for i in range(3):
        colors[..., i] = start_rgb[i] + normalized * (end_rgb[i] - start_rgb[i])

    return colors

def choose_color(parent, current_color_hex, title):
    """カラーパレットを表示して色を選択する関数"""
    color_code = colorchooser.askcolor(
        color=current_color_hex,
        title=title
    )
    if color_code[1]:
        return color_code[1]
    return None # 色が選択されなかった場合はNoneを返す
