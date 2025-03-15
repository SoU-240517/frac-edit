"""
パフォーマンステスト

このモジュールは、フラクタルジェネレータのパフォーマンスをテストします。
"""

import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core import (
    MandelbrotJulia, IterationColoring, ContinuousPotentialColoring,
    GradientGenerator, FractalRenderer
)

def test_fractal_calculation_performance():
    """
    フラクタル計算のパフォーマンスをテストする関数
    
    様々な解像度とパラメータでフラクタル計算のパフォーマンスを測定します。
    """
    print("フラクタル計算パフォーマンステスト")
    print("-" * 40)
    
    # テストする解像度
    resolutions = [
        (320, 240),    # 低解像度
        (640, 480),    # 標準解像度
        (1280, 720),   # HD
        (1920, 1080),  # フルHD
    ]
    
    # テストする反復回数
    iterations = [50, 100, 200, 500]
    
    # 結果を格納する辞書
    results = {}
    
    for width, height in resolutions:
        results[(width, height)] = {}
        
        for max_iter in iterations:
            # フラクタルオブジェクトを作成
            fractal = MandelbrotJulia(width, height)
            fractal.set_params({'max_iter': max_iter})
            
            # 計算時間を測定
            start_time = time.time()
            fractal_data = fractal.calculate(-2.0, 1.0, -1.5, 1.5)
            elapsed_time = time.time() - start_time
            
            # 結果を記録
            results[(width, height)][max_iter] = elapsed_time
            
            print(f"解像度: {width}x{height}, 反復回数: {max_iter}, 計算時間: {elapsed_time:.3f}秒")
    
    # 結果をグラフ化
    plt.figure(figsize=(10, 6))
    
    for i, (width, height) in enumerate(resolutions):
        plt.subplot(2, 2, i + 1)
        plt.title(f"解像度: {width}x{height}")
        plt.plot(iterations, [results[(width, height)][iter_val] for iter_val in iterations], 'o-')
        plt.xlabel("反復回数")
        plt.ylabel("計算時間 (秒)")
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "fractal_calculation_performance.png"))
    
    return results

def test_rendering_performance():
    """
    レンダリングのパフォーマンスをテストする関数
    
    様々な解像度とカラーリングアルゴリズムでレンダリングのパフォーマンスを測定します。
    """
    print("\nレンダリングパフォーマンステスト")
    print("-" * 40)
    
    # テストする解像度
    resolutions = [
        (320, 240),    # 低解像度
        (640, 480),    # 標準解像度
        (1280, 720),   # HD
        (1920, 1080),  # フルHD
    ]
    
    # テストするカラーリングアルゴリズム
    coloring_algorithms = {
        "反復回数": IterationColoring(),
        "連続的ポテンシャル": ContinuousPotentialColoring()
    }
    
    # グラデーションを作成
    gradient = GradientGenerator.create_preset_gradients()["rainbow"]
    
    # 結果を格納する辞書
    results = {}
    
    for width, height in resolutions:
        results[(width, height)] = {}
        
        # フラクタルオブジェクトを作成
        fractal = MandelbrotJulia(width, height)
        fractal.set_params({'max_iter': 100})
        
        # レンダラーを作成
        renderer = FractalRenderer(width, height)
        
        # フラクタルを計算
        fractal_data = fractal.calculate(-2.0, 1.0, -1.5, 1.5)
        
        for algo_name, algorithm in coloring_algorithms.items():
            # レンダリング時間を測定
            start_time = time.time()
            image = renderer.render(
                fractal,
                -2.0, 1.0, -1.5, 1.5,
                algorithm,
                gradient
            )
            elapsed_time = time.time() - start_time
            
            # 結果を記録
            results[(width, height)][algo_name] = elapsed_time
            
            print(f"解像度: {width}x{height}, アルゴリズム: {algo_name}, レンダリング時間: {elapsed_time:.3f}秒")
    
    # 結果をグラフ化
    plt.figure(figsize=(10, 6))
    
    for i, (width, height) in enumerate(resolutions):
        plt.subplot(2, 2, i + 1)
        plt.title(f"解像度: {width}x{height}")
        
        algo_names = list(coloring_algorithms.keys())
        times = [results[(width, height)][algo] for algo in algo_names]
        
        plt.bar(algo_names, times)
        plt.xlabel("カラーリングアルゴリズム")
        plt.ylabel("レンダリング時間 (秒)")
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "rendering_performance.png"))
    
    return results

def test_high_resolution_rendering():
    """
    高解像度レンダリングのパフォーマンスをテストする関数
    
    様々なオーバーサンプリング設定で高解像度レンダリングのパフォーマンスを測定します。
    """
    print("\n高解像度レンダリングパフォーマンステスト")
    print("-" * 40)
    
    # 解像度
    width, height = 1920, 1080
    
    # テストするオーバーサンプリング倍率
    oversample_factors = [1, 2, 4]
    
    # グラデーションを作成
    gradient = GradientGenerator.create_preset_gradients()["rainbow"]
    
    # 結果を格納する辞書
    results = {}
    
    # フラクタルオブジェクトを作成
    fractal = MandelbrotJulia(width, height)
    fractal.set_params({'max_iter': 100})
    
    # レンダラーを作成
    renderer = FractalRenderer(width, height)
    
    # カラーリングアルゴリズム
    coloring = IterationColoring()
    
    for oversample in oversample_factors:
        # レンダリング時間を測定
        start_time = time.time()
        image = renderer.render_high_quality(
            fractal,
            -2.0, 1.0, -1.5, 1.5,
            coloring,
            gradient,
            oversample=oversample
        )
        elapsed_time = time.time() - start_time
        
        # 結果を記録
        results[oversample] = elapsed_time
        
        print(f"解像度: {width}x{height}, オーバーサンプリング: {oversample}x, レンダリング時間: {elapsed_time:.3f}秒")
    
    # 結果をグラフ化
    plt.figure(figsize=(8, 5))
    plt.title("高解像度レンダリングパフォーマンス")
    plt.bar([f"{factor}x" for factor in oversample_factors], [results[factor] for factor in oversample_factors])
    plt.xlabel("オーバーサンプリング倍率")
    plt.ylabel("レンダリング時間 (秒)")
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "high_resolution_performance.png"))
    
    return results

def test_parallel_rendering():
    """
    並列レンダリングのパフォーマンスをテストする関数
    
    様々なスレッド数で並列レンダリングのパフォーマンスを測定します。
    """
    print("\n並列レンダリングパフォーマンステスト")
    print("-" * 40)
    
    # 解像度
    width, height = 1920, 1080
    
    # テストするスレッド数
    thread_counts = [1, 2, 4, 8]
    
    # グラデーションを作成
    gradient = GradientGenerator.create_preset_gradients()["rainbow"]
    
    # 結果を格納する辞書
    results = {}
    
    # フラクタルオブジェクトを作成
    fractal = MandelbrotJulia(width, height)
    fractal.set_params({'max_iter': 100})
    
    # レンダラーを作成
    renderer = FractalRenderer(width, height)
    
    # カラーリングアルゴリズム
    coloring = IterationColoring()
    
    for threads in thread_counts:
        # レンダリング時間を測定
        start_time = time.time()
        image = renderer.render_parallel(
            fractal,
            -2.0, 1.0, -1.5, 1.5,
            coloring,
            gradient,
            num_threads=threads
        )
        elapsed_time = time.time() - start_time
        
        # 結果を記録
        results[threads] = elapsed_time
        
        print(f"解像度: {width}x{height}, スレッド数: {threads}, レンダリング時間: {elapsed_time:.3f}秒")
    
    # 結果をグラフ化
    plt.figure(figsize=(8, 5))
    plt.title("並列レンダリングパフォーマンス")
    plt.plot(thread_counts, [results[threads] for threads in thread_counts], 'o-')
    plt.xlabel("スレッド数")
    plt.ylabel("レンダリング時間 (秒)")
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "parallel_rendering_performance.png"))
    
    return results

def run_all_tests():
    """
    すべてのパフォーマンステストを実行する関数
    """
    # テスト結果を格納するディレクトリを作成
    test_dir = os.path.dirname(__file__)
    os.makedirs(test_dir, exist_ok=True)
    
    # 各テストを実行
    calc_results = test_fractal_calculation_performance()
    render_results = test_rendering_performance()
    high_res_results = test_high_resolution_rendering()
    parallel_results = test_parallel_rendering()
    
    # 結果をまとめたレポートを作成
    report_path = os.path.join(test_dir, "performance_report.txt")
    
    with open(report_path, "w") as f:
        f.write("フラクタルジェネレータ パフォーマンステストレポート\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("1. フラクタル計算パフォーマンス\n")
        f.write("-" * 30 + "\n")
        for (width, height), iter_results in calc_results.items():
            f.write(f"解像度: {width}x{height}\n")
            for max_iter, time_taken in iter_results.items():
                f.write(f"  反復回数: {max_iter}, 計算時間: {time_taken:.3f}秒\n")
            f.write("\n")
        
        f.write("\n2. レンダリングパフォーマンス\n")
        f.write("-" * 30 + "\n")
        for (width, height), algo_results in render_results.items():
            f.write(f"解像度: {width}x{height}\n")
            for algo_name, time_taken in algo_results.items():
                f.write(f"  アルゴリズム: {algo_name}, レンダリング時間: {time_taken:.3f}秒\n")
            f.write("\n")
        
        f.write("\n3. 高解像度レンダリングパフォーマンス\n")
        f.write("-" * 30 + "\n")
        for oversample, time_taken in high_res_results.items():
            f.write(f"オーバーサンプリング: {oversample}x, レンダリング時間: {time_taken:.3f}秒\n")
        
        f.write("\n4. 並列レンダリングパフォーマンス\n")
        f.write("-" * 30 + "\n")
        for threads, time_taken in parallel_results.items():
            f.write(f"スレッド数: {threads}, レンダリング時間: {time_taken:.3f}秒\n")
    
    print(f"\nパフォーマンステストレポートが作成されました: {report_path}")
    print(f"グラフ画像は {test_dir} ディレクトリに保存されています")

if __name__ == "__main__":
    run_all_tests()
