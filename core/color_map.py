import numpy as np
from tkinter import colorchooser

def hex_to_rgb(hex_color): # --- 16進数カラーコードをRGB値に変換する関数 ---
    hex_color = hex_color.lstrip('#') # '#' を除去
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) # RGB値を返す

def is_valid_hex_color(color): # --- 16進数カラーコードの形式を検証する関数 ---
    if not color.startswith('#'): # '#' で始まっていない場合はFalseを返す
        return False
    try: # 16進数に変換できるか試す
        int(color[1:], 16) # '#' を除いて16進数に変換
        return len(color) == 7 # 6文字の16進数であるかを返す
    except ValueError: # 変換できない場合はFalseを返す
        return False

def create_colormap(values, start_color_hex, end_color_hex, bg_color_hex):  # --- 数値データからRGBカラーマップを生成 ---
    try:  # カラーコードをRGBに変換
        start_rgb = hex_to_rgb(start_color_hex)  # 開始色
        end_rgb = hex_to_rgb(end_color_hex)  # 終了色
        bg_rgb = hex_to_rgb(bg_color_hex)  # 背景色
    except:  # 変換に失敗したらデフォルト値を使用
        start_rgb = (0, 0, 255)  # 開始色を青に設定
        end_rgb = (255, 255, 255)  # 終了色を白に設定
        bg_rgb = (0, 0, 0)  # 背景色を黒に設定
    if len(values.shape) != 2:  # 入力が2次元配列か確認
        raise ValueError(f"Expected 2D values array, got shape {values.shape}")
    colors = np.full((values.shape[0], values.shape[1], 3), bg_rgb, dtype=np.uint8)  # 全ピクセルを背景色で埋めたRGB配列を初期化
    mask = values > 0  # 正の値を持つピクセルを選択
    normalized = np.where(mask, values, 0)  # 正の値はそのまま、0以下は0に
    for i in range(3):  # RGBの各成分（赤、緑、青）に対して
        colors[mask, i] = start_rgb[i] + normalized[mask] * (end_rgb[i] - start_rgb[i])  # 正の値に開始色から終了色へのグラデーションを適用
    return colors  # 生成したカラーマップを返す

def choose_color(parent, current_color_hex, title): # --- カラーパレットを表示して色を選択する関数 ---
    color_code = colorchooser.askcolor( # カラーパレットを表示
        color=current_color_hex, # 現在の色を設定
        title=title # タイトルを設定
    )
    if color_code[1]: # 色が選択された場合
        return color_code[1] # 選択された色を返す
    return None # 色が選択されなかった場合はNoneを返す
