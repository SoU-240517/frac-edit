import numpy as np

def calculate_julia(x_min, x_max, y_min, y_max, width, height, c_real, c_imag, max_iter, skip):
    """
    ジュリア集合を計算し、各点の繰り返し回数とポテンシャル値を返す関数

    Args:
        x_min, x_max, y_min, y_max: 描画領域の範囲
        width, height: 描画領域の幅と高さ
        c_real, c_imag: ジュリア集合のパラメータ c の実部と虚部
        max_iter: 最大繰り返し回数
        skip: 間引き数

    Returns:
        iterations: 各点の繰り返し回数のnumpy配列
        potentials: 各点のポテンシャル値のnumpy配列
    """

    x_coords = np.linspace(x_min, x_max, width // skip)
    y_coords = np.linspace(y_min, y_max, height // skip)
    c = complex(c_real, c_imag)

    iterations = np.zeros((height // skip, width // skip), dtype=np.int32)
    potentials = np.zeros((height // skip, width // skip), dtype=np.float64)

    for iy, y in enumerate(y_coords):
        for ix, x in enumerate(x_coords):
            z = complex(x, y)
            for i in range(max_iter):
                z = z * z + c
                if abs(z) > 2.0:
                    iterations[iy, ix] = i
                    # ポテンシャル関数の計算
                    potential = (np.log2(abs(z)) / (2**(i)))
                    potentials[iy, ix] = potential
                    break
            else:
                potentials[iy,ix] = 0

    return iterations, potentials
