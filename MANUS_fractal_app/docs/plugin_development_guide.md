# フラクタルジェネレータ プラグイン開発ガイド

## はじめに

このガイドでは、フラクタルジェネレータのプラグイン開発方法について説明します。プラグインを作成することで、新しいフラクタルタイプ、バリエーション、カラーリングアルゴリズムなどを追加できます。

## 目次

1. [プラグインシステムの概要](#プラグインシステムの概要)
2. [開発環境のセットアップ](#開発環境のセットアップ)
3. [プラグインの基本構造](#プラグインの基本構造)
4. [フラクタルタイププラグインの作成](#フラクタルタイププラグインの作成)
5. [バリエーションプラグインの作成](#バリエーションプラグインの作成)
6. [カラーリングアルゴリズムプラグインの作成](#カラーリングアルゴリズムプラグインの作成)
7. [プラグインのテスト](#プラグインのテスト)
8. [プラグインの配布](#プラグインの配布)
9. [サンプルプラグイン](#サンプルプラグイン)
10. [よくある質問](#よくある質問)

## プラグインシステムの概要

フラクタルジェネレータのプラグインシステムは、Pythonのモジュール機能を利用しています。プラグインは特定のインターフェースを実装したPythonクラスとして作成します。

### プラグインの種類

1. **フラクタルタイププラグイン**：新しいフラクタル計算アルゴリズムを追加
2. **バリエーションプラグイン**：新しい形状変換関数を追加
3. **カラーリングアルゴリズムプラグイン**：新しい色付け方法を追加

### プラグインの読み込み

プラグインは以下のディレクトリに配置することで自動的に読み込まれます：

- フラクタルタイププラグイン：`plugins/fractals/`
- バリエーションプラグイン：`plugins/variations/`
- カラーリングプラグイン：`plugins/coloring/`

## 開発環境のセットアップ

### 必要なツール

- Python 3.8以上
- テキストエディタまたはIDE（Visual Studio Code、PyCharmなど）
- フラクタルジェネレータ本体

### 開発環境の準備

1. フラクタルジェネレータをインストールします
2. プラグイン開発用のディレクトリを作成します：

```bash
mkdir -p my_fractal_plugin/plugins/fractals
mkdir -p my_fractal_plugin/plugins/variations
mkdir -p my_fractal_plugin/plugins/coloring
```

3. 必要なライブラリをインストールします：

```bash
pip install numpy scipy matplotlib pillow
```

## プラグインの基本構造

すべてのプラグインは、以下の基本構造に従います：

1. 適切なベースクラスを継承
2. メタデータを定義（名前、説明、バージョンなど）
3. 必要なメソッドをオーバーライド
4. プラグインマネージャーに登録するためのエントリーポイントを提供

### プラグインのメタデータ

各プラグインは以下のメタデータを定義する必要があります：

```python
class MyPlugin(BasePluginClass):
    """プラグインの説明"""
    
    # メタデータ
    NAME = "プラグイン名"
    DESCRIPTION = "プラグインの詳細な説明"
    VERSION = "1.0.0"
    AUTHOR = "作者名"
```

## フラクタルタイププラグインの作成

フラクタルタイププラグインは、`FractalBase`クラスを継承して作成します。

### 基本的な実装

```python
from src.core.fractal_base import FractalBase
import numpy as np

class MyFractal(FractalBase):
    """カスタムフラクタルの実装"""
    
    # メタデータ
    NAME = "マイフラクタル"
    DESCRIPTION = "カスタムフラクタルアルゴリズム"
    VERSION = "1.0.0"
    AUTHOR = "あなたの名前"
    
    def __init__(self, width, height):
        """初期化メソッド"""
        super().__init__(width, height)
        
        # デフォルトパラメータ
        self.params = {
            'max_iter': 100,
            'escape_radius': 2.0,
            'custom_param': 1.5
        }
    
    def calculate(self, x_min, x_max, y_min, y_max):
        """フラクタル計算の実装"""
        # 座標グリッドを作成
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_max, y_min, self.height)
        X, Y = np.meshgrid(x, y)
        
        # 複素数グリッドを作成
        C = X + 1j * Y
        
        # 初期値
        Z = np.zeros_like(C)
        
        # 結果を格納する配列
        result = np.zeros((self.height, self.width), dtype=np.float64)
        
        # パラメータを取得
        max_iter = self.params['max_iter']
        escape_radius = self.params['escape_radius']
        custom_param = self.params['custom_param']
        
        # フラクタル計算
        for i in range(max_iter):
            # カスタムアルゴリズムを実装
            Z = Z**2 + C * custom_param
            
            # 発散したポイントを記録
            mask = np.abs(Z) > escape_radius
            result[mask & (result == 0)] = i
            
            # すでに発散したポイントの計算をスキップ
            Z[mask] = 0
        
        return result
```

### パラメータの定義

ユーザーが調整できるパラメータは、`params`ディクショナリで定義します：

```python
self.params = {
    'パラメータ名': デフォルト値,
    # 他のパラメータ...
}
```

### UIとの連携

フラクタルタイププラグインがUIに表示されるようにするには、以下のメソッドを実装します：

```python
def get_param_info(self):
    """パラメータ情報を返す"""
    return {
        'max_iter': {
            'name': '反復回数',
            'type': 'int',
            'min': 10,
            'max': 1000,
            'step': 10
        },
        'custom_param': {
            'name': 'カスタムパラメータ',
            'type': 'float',
            'min': 0.1,
            'max': 5.0,
            'step': 0.1
        }
    }
```

## バリエーションプラグインの作成

バリエーションプラグインは、`VariationBase`クラスを継承して作成します。

### 基本的な実装

```python
from src.core.variation_base import VariationBase
import numpy as np

class MyVariation(VariationBase):
    """カスタムバリエーションの実装"""
    
    # メタデータ
    NAME = "マイバリエーション"
    DESCRIPTION = "カスタム形状変換"
    VERSION = "1.0.0"
    AUTHOR = "あなたの名前"
    
    def apply(self, points, weight=1.0):
        """バリエーションを適用"""
        # 入力は (N, 2) の形状の numpy 配列
        # 各行は [x, y] 座標
        
        # 点の座標を取得
        x, y = points[:, 0], points[:, 1]
        
        # 極座標に変換
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        # カスタム変換を適用
        r_new = r * np.sin(theta)
        theta_new = theta * np.cos(r)
        
        # 直交座標に戻す
        x_new = r_new * np.cos(theta_new)
        y_new = r_new * np.sin(theta_new)
        
        # 結果を重み付けして返す
        result = np.column_stack((x_new, y_new))
        return weight * result
```

### パラメータの追加

バリエーションにパラメータを追加するには：

```python
def __init__(self):
    """初期化メソッド"""
    super().__init__()
    
    # デフォルトパラメータ
    self.params = {
        'intensity': 1.0,
        'twist': 0.5
    }

def apply(self, points, weight=1.0):
    """バリエーションを適用"""
    # パラメータを取得
    intensity = self.params['intensity']
    twist = self.params['twist']
    
    # 以下、変換処理...
```

## カラーリングアルゴリズムプラグインの作成

カラーリングアルゴリズムプラグインは、`ColoringBase`クラスを継承して作成します。

### 基本的な実装

```python
from src.core.coloring_base import ColoringBase
import numpy as np

class MyColoring(ColoringBase):
    """カスタムカラーリングアルゴリズムの実装"""
    
    # メタデータ
    NAME = "マイカラーリング"
    DESCRIPTION = "カスタム色付けアルゴリズム"
    VERSION = "1.0.0"
    AUTHOR = "あなたの名前"
    
    def __init__(self):
        """初期化メソッド"""
        super().__init__()
        
        # デフォルトパラメータ
        self.params = {
            'frequency': 0.1,
            'phase': 0.0
        }
    
    def apply(self, fractal_data, gradient):
        """カラーリングを適用"""
        # fractal_data: フラクタル計算の結果（2D配列）
        # gradient: グラデーション関数 (0.0～1.0の値を受け取り、RGBAタプルを返す)
        
        # パラメータを取得
        frequency = self.params['frequency']
        phase = self.params['phase']
        
        # 正規化された値を計算
        max_val = np.max(fractal_data)
        if max_val > 0:
            normalized = fractal_data / max_val
        else:
            normalized = fractal_data
        
        # カスタムカラーマッピング
        color_index = np.sin(normalized * frequency * 2 * np.pi + phase) * 0.5 + 0.5
        
        # 画像データを作成（RGBA）
        height, width = fractal_data.shape
        image_data = np.zeros((height, width, 4), dtype=np.uint8)
        
        # 各ピクセルに色を適用
        for y in range(height):
            for x in range(width):
                if fractal_data[y, x] > 0:  # 発散した点
                    idx = color_index[y, x]
                    image_data[y, x] = gradient(idx)
                else:  # 収束した点（内部）
                    image_data[y, x] = (0, 0, 0, 255)  # 黒
        
        return image_data
```

## プラグインのテスト

### テスト用スクリプト

プラグインをテストするための簡単なスクリプトを作成できます：

```python
import sys
import os
import numpy as np
from PIL import Image

# プラグインディレクトリをパスに追加
sys.path.append('/path/to/fractal_generator')

# プラグインをインポート
from plugins.fractals.my_fractal import MyFractal
from src.core.coloring import IterationColoring
from src.core.renderer import FractalRenderer

def test_fractal_plugin():
    """フラクタルプラグインのテスト"""
    # フラクタルオブジェクトを作成
    width, height = 800, 600
    fractal = MyFractal(width, height)
    
    # パラメータを設定
    fractal.set_params({
        'max_iter': 100,
        'custom_param': 2.0
    })
    
    # カラーリングとレンダラーを作成
    coloring = IterationColoring()
    renderer = FractalRenderer(width, height)
    
    # レンダリング
    image = renderer.render(
        fractal,
        -2.0, 1.0, -1.5, 1.5,
        coloring
    )
    
    # 画像を保存
    image.save('test_output.png')
    print("テスト画像が保存されました: test_output.png")

if __name__ == "__main__":
    test_fractal_plugin()
```

### デバッグのヒント

1. `print`文を使用して中間結果を確認する
2. 小さな解像度（例：100x100）でテストして処理時間を短縮する
3. NumPyの配列形状を確認する：`print(array.shape)`
4. エラーが発生した場合は例外のスタックトレースを確認する

## プラグインの配布

### プラグインパッケージの作成

プラグインを配布するには、以下のファイル構造を作成します：

```
my_plugin/
├── README.md
├── plugin_info.json
└── plugins/
    ├── fractals/
    │   └── my_fractal.py
    ├── variations/
    │   └── my_variation.py
    └── coloring/
        └── my_coloring.py
```

`plugin_info.json`の例：

```json
{
  "name": "マイプラグインパック",
  "version": "1.0.0",
  "author": "あなたの名前",
  "description": "カスタムフラクタルとバリエーションを追加するプラグイン",
  "requires": "1.0.0",
  "components": [
    {
      "type": "fractal",
      "name": "マイフラクタル",
      "file": "plugins/fractals/my_fractal.py"
    },
    {
      "type": "variation",
      "name": "マイバリエーション",
      "file": "plugins/variations/my_variation.py"
    }
  ]
}
```

### プラグインのインストール方法

1. プラグインパッケージをZIPファイルに圧縮
2. フラクタルジェネレータの「プラグイン管理」画面を開く
3. 「プラグインのインストール」ボタンをクリック
4. ZIPファイルを選択
5. インストール完了後、アプリケーションを再起動

## サンプルプラグイン

### サンプルフラクタル：マンデルボックス

```python
from src.core.fractal_base import FractalBase
import numpy as np

class MandelboxFractal(FractalBase):
    """マンデルボックスフラクタル"""
    
    NAME = "マンデルボックス"
    DESCRIPTION = "3次元フラクタルの2次元スライス"
    VERSION = "1.0.0"
    AUTHOR = "サンプル作者"
    
    def __init__(self, width, height):
        """初期化メソッド"""
        super().__init__(width, height)
        
        self.params = {
            'max_iter': 20,
            'scale': 2.0,
            'bailout': 4.0
        }
    
    def calculate(self, x_min, x_max, y_min, y_max):
        """フラクタル計算の実装"""
        # 座標グリッドを作成
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_max, y_min, self.height)
        X, Y = np.meshgrid(x, y)
        
        # 結果を格納する配列
        result = np.zeros((self.height, self.width), dtype=np.float64)
        
        # パラメータを取得
        max_iter = self.params['max_iter']
        scale = self.params['scale']
        bailout = self.params['bailout']
        
        # 各ピクセルで計算
        for i in range(self.height):
            for j in range(self.width):
                # 初期値
                x, y, z = 0.0, 0.0, 0.0
                cx, cy = X[i, j], Y[i, j]
                cz = 0.0  # 2次元スライス
                
                # マンデルボックス反復
                for n in range(max_iter):
                    # ボックスフォールド
                    x = self._box_fold(x)
                    y = self._box_fold(y)
                    z = self._box_fold(z)
                    
                    # 球フォールド
                    r2 = x*x + y*y + z*z
                    if r2 < 0.25:
                        x, y, z = x*4, y*4, z*4
                    elif r2 < 1.0:
                        x, y, z = x/r2, y/r2, z/r2
                    
                    # スケーリングと移動
                    x = x * scale + cx
                    y = y * scale + cy
                    z = z * scale + cz
                    
                    # 発散チェック
                    if x*x + y*y + z*z > bailout:
                        result[i, j] = n + 1 - np.log(np.log(x*x + y*y + z*z)) / np.log(2)
                        break
        
        return result
    
    def _box_fold(self, v):
        """ボックスフォールド操作"""
        if v > 1.0:
            v = 2.0 - v
        elif v < -1.0:
            v = -2.0 - v
        return v
```

### サンプルバリエーション：スパイラル

```python
from src.core.variation_base import VariationBase
import numpy as np

class SpiralVariation(VariationBase):
    """スパイラルバリエーション"""
    
    NAME = "スパイラル"
    DESCRIPTION = "螺旋状の変形を適用"
    VERSION = "1.0.0"
    AUTHOR = "サンプル作者"
    
    def __init__(self):
        """初期化メソッド"""
        super().__init__()
        
        self.params = {
            'density': 1.0
        }
    
    def apply(self, points, weight=1.0):
        """バリエーションを適用"""
        # 点の座標を取得
        x, y = points[:, 0], points[:, 1]
        
        # 極座標に変換
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        # パラメータを取得
        density = self.params['density']
        
        # スパイラル変換
        r_new = r * (np.cos(theta * density) + np.sin(theta * density))
        theta_new = theta + r
        
        # 直交座標に戻す
        x_new = r_new * np.cos(theta_new)
        y_new = r_new * np.sin(theta_new)
        
        # 結果を重み付けして返す
        result = np.column_stack((x_new, y_new))
        return weight * result
```

## よくある質問

### Q: プラグインが読み込まれない場合はどうすればよいですか？

A: 以下を確認してください：
- プラグインファイルが正しいディレクトリにあるか
- クラス名とファイル名が一致しているか
- 必要なメタデータ（NAME, DESCRIPTION, VERSION, AUTHOR）が定義されているか
- 必須メソッドがすべて実装されているか
- 構文エラーがないか

### Q: プラグインの開発に必要な数学的知識はどの程度ですか？

A: フラクタルタイププラグインには複素数論や反復系の基本的な理解が必要です。バリエーションプラグインには座標変換の知識が役立ちます。ただし、既存のプラグインを参考にすれば、数学の詳細を完全に理解していなくても開発は可能です。

### Q: プラグインのパフォーマンスを向上させるにはどうすればよいですか？

A: 以下の方法を試してください：
- NumPyのベクトル化操作を最大限活用する
- ループ内での計算を最小限に抑える
- 不要な配列のコピーを避ける
- 計算量の多い処理は事前に最適化する
- 必要に応じてJITコンパイラ（Numba）を使用する

### Q: プラグインのデバッグ方法を教えてください

A: デバッグには以下の方法が有効です：
- 小さなテストケースから始める
- 中間結果を出力して確認する
- 例外処理を追加して詳細なエラーメッセージを表示する
- 単体テストを作成する
- Python のデバッガ（pdb）を使用する

### Q: 他の人のプラグインを改変して配布してもよいですか？

A: オリジナルのプラグインのライセンスに従ってください。多くの場合、著作者のクレジットを明記し、変更点を記録することで許可されています。不明な場合は、オリジナルの作者に確認することをお勧めします。

---

このガイドは、フラクタルジェネレータのプラグイン開発の基本を説明しています。さらに詳しい情報や高度なトピックについては、アプリケーションのヘルプメニューまたは開発者ドキュメントをご参照ください。
