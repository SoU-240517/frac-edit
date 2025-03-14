import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from numba import jit
import colorsys

@jit(nopython=True)
def julia_set(h, w, c, max_iterations):
    """ジュリア集合を計算する関数"""
    y, x = np.ogrid[-1.5:1.5:h*1j, -1.5:1.5:w*1j]
    z = x + y*1j
    divtime = max_iterations + np.zeros(z.shape, dtype=np.int32)

    for i in range(max_iterations):
        z = z**2 + c
        diverge = z*np.conj(z) > 2**2
        div_now = diverge & (divtime == max_iterations)
        divtime[div_now] = i
        z[diverge] = 2

    return divtime

def create_custom_colormap(num_colors=256):
    """滑らかな色の遷移を持つカスタムカラーマップを作成"""
    colors = []
    for i in range(num_colors):
        # HSVからRGBへの変換（黄金色から青への遷移）
        if i < num_colors // 3:
            # オレンジから黄金色
            h = 0.05 + (0.1 * i / (num_colors // 3))
            s = 0.8
            v = 0.9
        elif i < 2 * (num_colors // 3):
            # 黄金色から青/ターコイズへ
            h = 0.15 + (0.4 * (i - num_colors // 3) / (num_colors // 3))
            s = 0.85 - (0.2 * (i - num_colors // 3) / (num_colors // 3))
            v = 0.9
        else:
            # 青/ターコイズから深い青へ
            h = 0.55 + (0.1 * (i - 2 * (num_colors // 3)) / (num_colors // 3))
            s = 0.65 + (0.2 * (i - 2 * (num_colors // 3)) / (num_colors // 3))
            v = 0.9 - (0.3 * (i - 2 * (num_colors // 3)) / (num_colors // 3))

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        colors.append((r, g, b))

    return LinearSegmentedColormap.from_list("custom", colors, N=num_colors)

def generate_fractal(width=1000, height=1000, c=-0.8 + 0.156j, max_iterations=300,
                     color_offset=0, zoom=1.0, center_x=0, center_y=0):
    """カスタマイズ可能なフラクタル画像を生成"""
    # ジュリア集合を計算
    fractal = julia_set(height, width, c, max_iterations)

    # カスタムカラーマップを作成
    cmap = create_custom_colormap(256)

    # 画像の保存
    plt.figure(figsize=(10, 10), dpi=100)
    plt.imshow(fractal, cmap=cmap, origin='lower')
    plt.axis('off')
    plt.tight_layout(pad=0)

    # 画像をファイルに保存
    filename = f"fractal_c_{c.real:.3f}_{c.imag:.3f}_iter_{max_iterations}.png"
    plt.savefig(filename, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()

    print(f"フラクタル画像を保存しました: {filename}")
    return filename

def interactive_fractal_explorer():
    """インタラクティブにパラメータを調整できるフラクタルエクスプローラー"""
    import tkinter as tk
    from tkinter import ttk
    from PIL import Image, ImageTk
    import io
    import matplotlib
    matplotlib.use("Agg")

    root = tk.Tk()
    root.title("フラクタルジェネレーター")

    # パラメータフレーム
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # パラメータコントロール
    ttk.Label(frame, text="実部 (c_real):").grid(column=0, row=0, sticky=tk.W)
    c_real_var = tk.DoubleVar(value=-0.8)
    c_real = ttk.Scale(frame, from_=-2.0, to=2.0, length=200, variable=c_real_var)
    c_real.grid(column=1, row=0)
    ttk.Label(frame, textvariable=c_real_var).grid(column=2, row=0)

    ttk.Label(frame, text="虚部 (c_imag):").grid(column=0, row=1, sticky=tk.W)
    c_imag_var = tk.DoubleVar(value=0.156)
    c_imag = ttk.Scale(frame, from_=-2.0, to=2.0, length=200, variable=c_imag_var)
    c_imag.grid(column=1, row=1)
    ttk.Label(frame, textvariable=c_imag_var).grid(column=2, row=1)

    ttk.Label(frame, text="最大反復回数:").grid(column=0, row=2, sticky=tk.W)
    max_iter_var = tk.IntVar(value=100)
    max_iter = ttk.Scale(frame, from_=10, to=500, length=200, variable=max_iter_var)
    max_iter.grid(column=1, row=2)
    ttk.Label(frame, textvariable=max_iter_var).grid(column=2, row=2)

    # イメージフレーム
    img_frame = ttk.Frame(root, padding="10")
    img_frame.grid(row=1, column=0)

    # 初期イメージプレースホルダー
    image_label = ttk.Label(img_frame)
    image_label.grid(row=0, column=0)

    # 生成用関数
    def update_image():
        c = complex(c_real_var.get(), c_imag_var.get())
        iterations = max_iter_var.get()

        fractal = julia_set(500, 500, c, iterations)
        cmap = create_custom_colormap(256)

        fig = plt.figure(figsize=(5, 5), dpi=100)
        plt.imshow(fractal, cmap=cmap, origin='lower')
        plt.axis('off')
        plt.tight_layout(pad=0)

        # イメージを保存してTkinterで表示
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        buf.seek(0)
        img = Image.open(buf)
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo  # 参照を保持

    # 生成ボタン
    gen_button = ttk.Button(frame, text="フラクタルを生成", command=update_image)
    gen_button.grid(column=1, row=3)

    # 保存ボタン
    def save_image():
        c = complex(c_real_var.get(), c_imag_var.get())
        iterations = max_iter_var.get()
        generate_fractal(1000, 1000, c, iterations)

    save_button = ttk.Button(frame, text="高解像度で保存", command=save_image)
    save_button.grid(column=1, row=4)

    # 初期画像を生成
    update_image()

    root.mainloop()

if __name__ == "__main__":
    # コマンドラインから直接使用する場合
    print("フラクタルジェネレーターを起動します")
    print("1: 単一のフラクタル画像を生成")
    print("2: インタラクティブエクスプローラーを起動")

    choice = input("選択してください (1 または 2): ")

    if choice == "1":
        # デフォルトパラメータでフラクタルを生成
        c_real = float(input("実部 (デフォルト: -0.8): ") or -0.8)
        c_imag = float(input("虚部 (デフォルト: 0.156): ") or 0.156)
        iterations = int(input("最大反復回数 (デフォルト: 300): ") or 300)

        generate_fractal(width=2000, height=2000, c=complex(c_real, c_imag), max_iterations=iterations)
    elif choice == "2":
        # インタラクティブエクスプローラーを起動
        interactive_fractal_explorer()
    else:
        print("無効な選択です。")
