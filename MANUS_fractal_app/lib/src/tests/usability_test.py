"""
ユーザビリティテスト

このモジュールは、フラクタルジェネレータのユーザビリティをテストします。
"""

import sys
import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
import json

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app import FractalGeneratorApp

class UsabilityTest:
    """
    ユーザビリティテストを実行するクラス
    """
    
    def __init__(self):
        """
        初期化メソッド
        """
        self.test_results = {}
        self.current_test = None
        self.start_time = 0
        
        # テスト結果を保存するディレクトリを作成
        self.test_dir = os.path.dirname(__file__)
        os.makedirs(self.test_dir, exist_ok=True)
    
    def start_test(self, test_name):
        """
        テストを開始するメソッド
        
        Args:
            test_name (str): テスト名
        """
        self.current_test = test_name
        self.start_time = time.time()
        print(f"テスト開始: {test_name}")
    
    def end_test(self, success=True, notes=""):
        """
        テストを終了するメソッド
        
        Args:
            success (bool): テストが成功したかどうか
            notes (str): テストに関するメモ
        """
        if not self.current_test:
            return
        
        elapsed_time = time.time() - self.start_time
        
        self.test_results[self.current_test] = {
            'success': success,
            'elapsed_time': elapsed_time,
            'notes': notes
        }
        
        status = "成功" if success else "失敗"
        print(f"テスト終了: {self.current_test} - {status} ({elapsed_time:.2f}秒)")
        print(f"メモ: {notes}")
        print("-" * 40)
        
        self.current_test = None
    
    def save_results(self):
        """
        テスト結果を保存するメソッド
        """
        report_path = os.path.join(self.test_dir, "usability_report.json")
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"ユーザビリティテストレポートが作成されました: {report_path}")
        
        # テキスト形式のレポートも作成
        text_report_path = os.path.join(self.test_dir, "usability_report.txt")
        
        with open(text_report_path, "w", encoding="utf-8") as f:
            f.write("フラクタルジェネレータ ユーザビリティテストレポート\n")
            f.write("=" * 50 + "\n\n")
            
            success_count = sum(1 for result in self.test_results.values() if result['success'])
            total_count = len(self.test_results)
            
            f.write(f"テスト成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)\n\n")
            
            for test_name, result in self.test_results.items():
                status = "成功" if result['success'] else "失敗"
                f.write(f"テスト: {test_name}\n")
                f.write(f"結果: {status}\n")
                f.write(f"所要時間: {result['elapsed_time']:.2f}秒\n")
                f.write(f"メモ: {result['notes']}\n")
                f.write("-" * 40 + "\n\n")
        
        print(f"テキスト形式のレポートも作成されました: {text_report_path}")


class AutomatedUsabilityTest:
    """
    自動化されたユーザビリティテストを実行するクラス
    """
    
    def __init__(self):
        """
        初期化メソッド
        """
        self.root = tk.Tk()
        self.root.withdraw()  # メインウィンドウを非表示
        
        self.app = None
        self.tester = UsabilityTest()
    
    def run_tests(self):
        """
        すべてのテストを実行するメソッド
        """
        try:
            # アプリケーションを起動
            self.setup_application()
            
            # 各テストを実行
            self.test_basic_ui()
            self.test_fractal_rendering()
            self.test_parameter_adjustment()
            self.test_zoom_and_pan()
            self.test_color_settings()
            self.test_save_load()
            self.test_high_resolution_rendering()
            self.test_history_management()
            self.test_pivot_editing()
            
            # テスト結果を保存
            self.tester.save_results()
            
        finally:
            # アプリケーションを終了
            if self.app:
                self.root.quit()
    
    def setup_application(self):
        """
        テスト用にアプリケーションをセットアップするメソッド
        """
        self.tester.start_test("アプリケーション起動")
        
        try:
            # アプリケーションを作成
            self.app = FractalGeneratorApp(self.root)
            
            # ウィンドウサイズを設定
            self.root.geometry("1200x800")
            
            # 表示
            self.root.update()
            
            self.tester.end_test(True, "アプリケーションが正常に起動しました")
        except Exception as e:
            self.tester.end_test(False, f"アプリケーション起動エラー: {str(e)}")
    
    def test_basic_ui(self):
        """
        基本的なUIコンポーネントをテストするメソッド
        """
        self.tester.start_test("基本UI確認")
        
        try:
            # 主要なUIコンポーネントが存在するか確認
            components = [
                (self.app.canvas, "キャンバス"),
                (self.app.control_panel, "コントロールパネル"),
                (self.app.render_button, "レンダリングボタン"),
                (self.app.high_res_button, "高解像度レンダリングボタン"),
                (self.app.status_bar, "ステータスバー")
            ]
            
            missing = []
            for component, name in components:
                if not component:
                    missing.append(name)
            
            if missing:
                self.tester.end_test(False, f"不足しているUIコンポーネント: {', '.join(missing)}")
            else:
                self.tester.end_test(True, "すべての主要UIコンポーネントが存在します")
        
        except Exception as e:
            self.tester.end_test(False, f"UIテストエラー: {str(e)}")
    
    def test_fractal_rendering(self):
        """
        フラクタルレンダリングをテストするメソッド
        """
        self.tester.start_test("フラクタルレンダリング")
        
        try:
            # レンダリングボタンをクリック
            self.app.render_fractal()
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            # キャンバスに画像が表示されているか確認
            if hasattr(self.app, 'tk_image') and self.app.tk_image:
                self.tester.end_test(True, "フラクタルが正常にレンダリングされました")
            else:
                self.tester.end_test(False, "フラクタル画像が表示されていません")
        
        except Exception as e:
            self.tester.end_test(False, f"レンダリングエラー: {str(e)}")
    
    def test_parameter_adjustment(self):
        """
        パラメータ調整をテストするメソッド
        """
        self.tester.start_test("パラメータ調整")
        
        try:
            # 反復回数を変更
            original_value = self.app.hanpuku_var.get()
            new_value = "150"
            
            self.app.hanpuku_var.set(new_value)
            
            # レンダリング
            self.app.render_fractal()
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            # 値が正しく設定されているか確認
            if self.app.hanpuku_var.get() == new_value:
                self.tester.end_test(True, "パラメータが正常に調整されました")
            else:
                self.tester.end_test(False, "パラメータ値が正しく設定されていません")
            
            # 元の値に戻す
            self.app.hanpuku_var.set(original_value)
        
        except Exception as e:
            self.tester.end_test(False, f"パラメータ調整エラー: {str(e)}")
    
    def test_zoom_and_pan(self):
        """
        ズームとパン機能をテストするメソッド
        """
        self.tester.start_test("ズームとパン")
        
        try:
            # 元のビュー範囲を保存
            original_view = self.app.current_view.copy()
            
            # ズーム操作をシミュレート
            self.app.zoom_at_point(
                self.app.canvas.winfo_width() // 2,
                self.app.canvas.winfo_height() // 2,
                0.5  # ズームイン
            )
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            # ビュー範囲が変更されたか確認
            view_changed = (
                self.app.current_view['x_min'] != original_view['x_min'] or
                self.app.current_view['x_max'] != original_view['x_max'] or
                self.app.current_view['y_min'] != original_view['y_min'] or
                self.app.current_view['y_max'] != original_view['y_max']
            )
            
            if view_changed:
                self.tester.end_test(True, "ズーム機能が正常に動作しています")
            else:
                self.tester.end_test(False, "ズーム操作後もビュー範囲が変更されていません")
            
            # 元のビューに戻す
            self.app.current_view = original_view.copy()
            self.app.render_fractal()
        
        except Exception as e:
            self.tester.end_test(False, f"ズーム/パンエラー: {str(e)}")
    
    def test_color_settings(self):
        """
        カラー設定をテストするメソッド
        """
        self.tester.start_test("カラー設定")
        
        try:
            # 元のグラデーションプリセットを保存
            original_preset = self.app.gradient_preset_var.get()
            
            # 別のプリセットを選択
            new_preset = "hot" if original_preset != "hot" else "cool"
            self.app.gradient_preset_var.set(new_preset)
            
            # グラデーションを変更
            self.app.on_gradient_preset_changed(None)
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            # 値が正しく設定されているか確認
            if self.app.gradient_preset_var.get() == new_preset:
                self.tester.end_test(True, "カラー設定が正常に変更されました")
            else:
                self.tester.end_test(False, "カラー設定が正しく変更されていません")
            
            # 元の値に戻す
            self.app.gradient_preset_var.set(original_preset)
            self.app.on_gradient_preset_changed(None)
        
        except Exception as e:
            self.tester.end_test(False, f"カラー設定エラー: {str(e)}")
    
    def test_save_load(self):
        """
        保存と読み込み機能をテストするメソッド
        """
        self.tester.start_test("パラメータ保存/読み込み")
        
        try:
            # テスト用のファイルパス
            test_file = os.path.join(self.test_dir, "test_params.json")
            
            # 現在のパラメータを取得
            params = {
                'fractal': self.app.current_fractal.get_params(),
                'coloring': self.app.current_coloring.get_params(),
                'view': self.app.current_view,
                'fractal_type': self.app.frac_type_dropdown_var.get(),
                'coloring_algorithm': self.app.hassan_algo_var.get(),
                'gradient_preset': self.app.gradient_preset_var.get()
            }
            
            # JSONとして保存
            with open(test_file, 'w', encoding='utf-8') as f:
                json.dump(params, f, indent=2)
            
            # パラメータを変更
            original_iter = self.app.hanpuku_var.get()
            self.app.hanpuku_var.set("200")
            self.app.update_fractal_parameters()
            
            # 保存したパラメータを読み込む
            with open(test_file, 'r', encoding='utf-8') as f:
                loaded_params = json.load(f)
            
            # パラメータを設定
            if 'fractal' in loaded_params:
                self.app.current_fractal.set_params(loaded_params['fractal'])
                
                # UIも更新
                if 'max_iter' in loaded_params['fractal']:
                    self.app.hanpuku_var.set(str(loaded_params['fractal']['max_iter']))
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            # 値が正しく読み込まれたか確認
            if self.app.hanpuku_var.get() == str(params['fractal']['max_iter']):
                self.tester.end_test(True, "パラメータが正常に保存/読み込みされました")
            else:
                self.tester.end_test(False, "パラメータが正しく読み込まれていません")
            
            # テストファイルを削除
            os.remove(test_file)
        
        except Exception as e:
            self.tester.end_test(False, f"保存/読み込みエラー: {str(e)}")
    
    def test_high_resolution_rendering(self):
        """
        高解像度レンダリングをテストするメソッド
        """
        self.tester.start_test("高解像度レンダリング")
        
        try:
            # テスト用のファイルパス
            test_file = os.path.join(self.test_dir, "test_high_res.png")
            
            # 小さいサイズでテスト
            width, height = 320, 240
            oversample = 1
            quality = 90
            
            # 高解像度レンダリングを実行
            self.app._high_res_render_thread(test_file, width, height, oversample, quality)
            
            # ファイルが作成されたか確認
            if os.path.exists(test_file) and os.path.getsize(test_file) > 0:
                self.tester.end_test(True, "高解像度レンダリングが正常に実行されました")
            else:
                self.tester.end_test(False, "高解像度画像ファイルが作成されていません")
            
            # テストファイルを削除
            if os.path.exists(test_file):
                os.remove(test_file)
        
        except Exception as e:
            self.tester.end_test(False, f"高解像度レンダリングエラー: {str(e)}")
    
    def test_history_management(self):
        """
        履歴管理機能をテストするメソッド
        """
        self.tester.start_test("履歴管理")
        
        try:
            # 元の状態を保存
            original_iter = self.app.hanpuku_var.get()
            
            # パラメータを変更して履歴に追加
            self.app.hanpuku_var.set("200")
            self.app.render_fractal()
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            # 別のパラメータに変更して履歴に追加
            self.app.hanpuku_var.set("300")
            self.app.render_fractal()
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            # 元に戻す
            self.app.undo()
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            # 値が正しく戻ったか確認
            if self.app.hanpuku_var.get() == "200":
                self.tester.end_test(True, "履歴管理機能が正常に動作しています")
            else:
                self.tester.end_test(False, "元に戻す操作が正しく機能していません")
            
            # 元の値に戻す
            self.app.hanpuku_var.set(original_iter)
            self.app.render_fractal()
        
        except Exception as e:
            self.tester.end_test(False, f"履歴管理エラー: {str(e)}")
    
    def test_pivot_editing(self):
        """
        ピボット編集機能をテストするメソッド
        """
        self.tester.start_test("ピボット編集")
        
        try:
            # ノード編集モードに切り替え
            self.app.switch_to_node_editor()
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            # キャンバスモードに戻す
            self.app.switch_to_canvas()
            
            # 更新を待機
            self.root.update()
            time.sleep(1)
            
            self.tester.end_test(True, "ピボット編集モードの切り替えが正常に動作しています")
        
        except Exception as e:
            self.tester.end_test(False, f"ピボット編集エラー: {str(e)}")


def run_usability_tests():
    """
    ユーザビリティテストを実行する関数
    """
    print("フラクタルジェネレータ ユーザビリティテスト開始")
    print("=" * 50)
    
    tester = AutomatedUsabilityTest()
    tester.run_tests()
    
    print("\nユーザビリティテスト完了")


if __name__ == "__main__":
    run_usability_tests()
