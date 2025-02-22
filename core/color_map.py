import numpy as np # NumPyライブラリをインポート
from tkinter import colorchooser # カラーパレットを表示するためのモジュール

# 16進数カラーコードをRGB値に変換する関数
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#') # '#' を除去
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) # RGB値を返す

# 16進数カラーコードの形式を検証する関数
def is_valid_hex_color(color):
    if not color.startswith('#'): # '#' で始まっていない場合はFalseを返す
        return False
    try: # 16進数に変換できるか試す
        int(color[1:], 16) # '#' を除いて16進数に変換
        return len(color) == 7 # 6文字の16進数であるかを返す
    except ValueError: # 変換できない場合はFalseを返す
        return False

# カラーマップを作成する関数
def create_colormap(values, start_color_hex, end_color_hex):
    try: # エラーの場合はデフォルトの色を使用
        start_rgb = hex_to_rgb(start_color_hex) # 開始色のRGB値を取得
        end_rgb = hex_to_rgb(end_color_hex) # 終了色のRGB値を取得
    except: # エラーの場合はデフォルトの色を使用
        start_rgb = (0, 0, 255) # 開始色を青に設定
        end_rgb = (255, 255, 255) # 終了色を白に設定

    colors = np.zeros((values.shape[0], values.shape[1], 3), dtype=np.uint8) # 配列を作成

    normalized = np.where(values > 0, values, 0) # 0以下の値を0に変換

    for i in range(3): # RGBの3色成分に対して繰り返す
        colors[..., i] = start_rgb[i] + normalized * (end_rgb[i] - start_rgb[i]) # グラデーションを計算

    return colors

# カラーパレットを表示して色を選択する関数
def choose_color(parent, current_color_hex, title):
    color_code = colorchooser.askcolor( # カラーパレットを表示
        color=current_color_hex, # 現在の色を設定
        title=title # タイトルを設定
    )
    if color_code[1]: # 色が選択された場合
        return color_code[1] # 選択された色を返す
    return None # 色が選択されなかった場合はNoneを返す
