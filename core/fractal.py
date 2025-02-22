import numpy as np  # NumPyライブラリをインポートする

# フラクタル図形の計算を行う関数を定義する
def calculate_julia(view_x_min, view_x_max, view_y_min, view_y_max, width, height, real, imag, max_iter, skip=1):
    x = np.linspace(view_x_min, view_x_max, width) # x軸の値を生成する
    y = np.linspace(view_y_min, view_y_max, height) # y軸の値を生成する
    X, Y = np.meshgrid(x[::skip], y[::skip]) # x軸とy軸の値を組み合わせる
    Z = X + Y*1j # 複素数を生成する

    c = complex(real, imag) # 複素数を生成する
    output = np.zeros(Z.shape, dtype=np.float32) # 出力用の配列を生成する

    for i in range(max_iter): # 最大繰り返し回数分繰り返す
        mask = np.abs(Z) <= 2 # 絶対値が2を超える要素を抽出する
        Z[mask] = Z[mask]**2 + c # マンデルブロ集合の計算を行う
        output[mask & (np.abs(Z) > 2)] = i + 1 - np.log2(np.log2(np.abs(Z[mask & (np.abs(Z) > 2)]))) # 出力用の配列に値を代入する

    # 正規化
    mask = output > 0 # 出力用の配列の値が0より大きい要素を抽出する
    if mask.any(): # 出力用の配列の値が0より大きい要素が存在する場合
        output[mask] = (output[mask] - output[mask].min()) / (output[mask].max() - output[mask].min()) # 出力用の配列を正規化する

    return output
