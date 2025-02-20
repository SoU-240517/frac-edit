import tkinter as tk
from ui.main_window import MainWindow   # MainWindowクラスのインポート

if __name__ == "__main__":  # このファイルが直接実行されたときに実行される
    root = tk.Tk()          # Tkクラスをインスタンス化
    app = MainWindow(root)  # MainWindowクラスをインスタンス化
    root.mainloop()         # イベントループを開始
