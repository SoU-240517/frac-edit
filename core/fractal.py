# julia_viewer/core/fractal.py
import numpy as np

def calculate_julia(view_x_min, view_x_max, view_y_min, view_y_max, width, height, real, imag, max_iter, skip=1):
    """Julia集合を計算する関数"""
    x = np.linspace(view_x_min, view_x_max, width)
    y = np.linspace(view_y_min, view_y_max, height)
    X, Y = np.meshgrid(x[::skip], y[::skip])
    Z = X + Y*1j

    c = complex(real, imag)
    output = np.zeros(Z.shape, dtype=np.float32)

    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask]**2 + c
        output[mask & (np.abs(Z) > 2)] = i + 1 - np.log2(np.log2(np.abs(Z[mask & (np.abs(Z) > 2)])))

    # 正規化
    mask = output > 0
    if mask.any():
        output[mask] = (output[mask] - output[mask].min()) / (output[mask].max() - output[mask].min())

    return output
