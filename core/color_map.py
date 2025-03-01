import numpy as np
from tkinter import colorchooser

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def is_valid_hex_color(color):
    if not color.startswith('#'):
        return False
    try:
        int(color[1:], 16)
        return len(color) == 7
    except ValueError:
        return False

def create_colormap(iterations, potentials, start_color_hex, end_color_hex, inner_color_hex):
    """
    繰り返し回数とポテンシャル値に基づいてカラーマップを生成する関数

    Args:
        iterations: 繰り返し回数のnumpy配列
        potentials: ポテンシャル値のnumpy配列
        start_color_hex: 発散開始色の16進数カラーコード
        end_color_hex: 発散終了色の16進数カラーコード
        inner_color_hex: 発散しない領域の色(内部の色)

    Returns:
        colors: カラーマップのnumpy配列
    """

    try:
        start_rgb = hex_to_rgb(start_color_hex)
        end_rgb = hex_to_rgb(end_color_hex)
        inner_rgb = hex_to_rgb(inner_color_hex)
    except:
        start_rgb = (0, 0, 255)
        end_rgb = (255, 255, 255)
        inner_rgb = (0, 0, 0)

    if len(iterations.shape) != 2 or len(potentials.shape) != 2:
        raise ValueError(f"Expected 2D values array, got iterations shape {iterations.shape} and potentials shape {potentials.shape}")

    colors = np.zeros((iterations.shape[0], iterations.shape[1], 3), dtype=np.uint8)

    #発散していない領域を塗る
    inner_mask = iterations == 0
    colors[inner_mask] = inner_rgb

    # 発散領域のグラデーション処理
    diverged_mask = iterations > 0
    normalized = potentials[diverged_mask]
    for i in range(3):
        colors[diverged_mask, i] = start_rgb[i] + normalized * (end_rgb[i] - start_rgb[i])

    return colors

def choose_color(parent, current_color_hex, title):
    color_code = colorchooser.askcolor(
        color=current_color_hex,
        title=title
    )
    if color_code[1]:
        return color_code[1]
    return None
