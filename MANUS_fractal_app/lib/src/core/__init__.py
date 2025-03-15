"""
フラクタルジェネレータのメインモジュール

このモジュールは、フラクタルジェネレータのコアコンポーネントをまとめます。
"""

from .fractal_base import FractalBase
from .mandelbrot_julia import MandelbrotJulia
from .plugin_manager import PluginManager, variation
from .coloring import ColoringAlgorithm, IterationColoring, ContinuousPotentialColoring, GradientGenerator
from .renderer import FractalRenderer

__all__ = [
    'FractalBase',
    'MandelbrotJulia',
    'PluginManager',
    'variation',
    'ColoringAlgorithm',
    'IterationColoring',
    'ContinuousPotentialColoring',
    'GradientGenerator',
    'FractalRenderer'
]
