"""
メインエントリーポイント

このモジュールは、フラクタルジェネレータのエントリーポイントを提供します。

フラクタルジェネレータのメインスクリプト（修正版）

このスクリプトは、フラクタルジェネレータアプリケーションを起動します。
修正版のapp_fixed.pyを使用して、スクロールバーの問題と'complex' object is not subscriptableエラーを解決しています。
"""

import os
import sys

# プロジェクトのルートディレクトリをPythonパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
lib_dir = os.path.join(root_dir, "lib")

# パスを追加
sys.path.insert(0, root_dir)
sys.path.insert(0, lib_dir)

# 修正版のアプリケーションをインポート
from lib.src.app_fixed import main

if __name__ == "__main__":
    main()
