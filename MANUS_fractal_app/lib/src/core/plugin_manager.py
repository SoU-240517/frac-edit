"""
プラグインシステムの基本実装

このモジュールは、フラクタルタイプとバリエーションをプラグインとして管理するシステムを提供します。
"""

import os
import importlib.util
import inspect
from .fractal_base import FractalBase

class PluginManager:
    """
    プラグインを管理するクラス
    
    フラクタルタイプとバリエーションのプラグインを読み込み、管理します。
    """
    
    def __init__(self, plugin_dir=None):
        """
        初期化メソッド
        
        Args:
            plugin_dir (str, optional): プラグインディレクトリのパス
        """
        self.plugin_dir = plugin_dir or os.path.join(os.path.dirname(__file__), '..', '..', 'plugins')
        self.fractal_types = {}  # フラクタルタイプのプラグイン
        self.variations = {}     # バリエーションのプラグイン
        
    def load_plugins(self):
        """
        プラグインディレクトリからプラグインを読み込みます
        
        Returns:
            tuple: (読み込まれたフラクタルタイプの数, 読み込まれたバリエーションの数)
        """
        # プラグインディレクトリが存在しない場合は作成
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            
        # フラクタルタイプのディレクトリ
        fractal_dir = os.path.join(self.plugin_dir, 'fractals')
        if not os.path.exists(fractal_dir):
            os.makedirs(fractal_dir)
            
        # バリエーションのディレクトリ
        variation_dir = os.path.join(self.plugin_dir, 'variations')
        if not os.path.exists(variation_dir):
            os.makedirs(variation_dir)
            
        # フラクタルタイププラグインを読み込む
        fractal_count = self._load_fractal_plugins(fractal_dir)
        
        # バリエーションプラグインを読み込む
        variation_count = self._load_variation_plugins(variation_dir)
        
        return fractal_count, variation_count
    
    def _load_fractal_plugins(self, directory):
        """
        フラクタルタイププラグインを読み込みます
        
        Args:
            directory (str): プラグインディレクトリのパス
            
        Returns:
            int: 読み込まれたプラグインの数
        """
        count = 0
        
        # ディレクトリ内のPythonファイルを検索
        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_path = os.path.join(directory, filename)
                module_name = os.path.splitext(filename)[0]
                
                try:
                    # モジュールを動的に読み込む
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # モジュール内のFractalBaseを継承したクラスを探す
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, FractalBase) and 
                            obj != FractalBase):
                            
                            # プラグインとして登録
                            self.fractal_types[name] = obj
                            count += 1
                            
                except Exception as e:
                    print(f"プラグイン '{module_name}' の読み込みに失敗しました: {e}")
        
        return count
    
    def _load_variation_plugins(self, directory):
        """
        バリエーションプラグインを読み込みます
        
        Args:
            directory (str): プラグインディレクトリのパス
            
        Returns:
            int: 読み込まれたプラグインの数
        """
        count = 0
        
        # ディレクトリ内のPythonファイルを検索
        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_path = os.path.join(directory, filename)
                module_name = os.path.splitext(filename)[0]
                
                try:
                    # モジュールを動的に読み込む
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # モジュール内の適切な関数を探す
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isfunction(obj) and 
                            hasattr(obj, 'is_variation') and 
                            obj.is_variation):
                            
                            # プラグインとして登録
                            self.variations[name] = obj
                            count += 1
                            
                except Exception as e:
                    print(f"バリエーション '{module_name}' の読み込みに失敗しました: {e}")
        
        return count
    
    def get_fractal_types(self):
        """
        利用可能なフラクタルタイプの一覧を取得します
        
        Returns:
            dict: フラクタルタイプ名とクラスのマッピング
        """
        return self.fractal_types
    
    def get_variations(self):
        """
        利用可能なバリエーションの一覧を取得します
        
        Returns:
            dict: バリエーション名と関数のマッピング
        """
        return self.variations
    
    def create_fractal(self, fractal_type, width, height):
        """
        指定されたフラクタルタイプのインスタンスを作成します
        
        Args:
            fractal_type (str): フラクタルタイプ名
            width (int): 画像の幅
            height (int): 画像の高さ
            
        Returns:
            FractalBase: フラクタルオブジェクト
            
        Raises:
            ValueError: 指定されたフラクタルタイプが存在しない場合
        """
        if fractal_type not in self.fractal_types:
            raise ValueError(f"フラクタルタイプ '{fractal_type}' は存在しません")
        
        return self.fractal_types[fractal_type](width, height)

# バリエーション関数を作成するためのデコレータ
def variation(func):
    """
    バリエーション関数を登録するためのデコレータ
    
    Args:
        func: バリエーション関数
        
    Returns:
        function: デコレートされた関数
    """
    func.is_variation = True
    return func
