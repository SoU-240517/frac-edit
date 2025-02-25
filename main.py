import tkinter as tk
from ui.main_window import MainWindow

if __name__ == "__main__": # もし、このファイルが直接実行されたときは、次を実行する
    root = tk.Tk() #  Tkinterのルートウィンドウを作成
    app = MainWindow(root) # MainWindowクラスのインスタンスを作成し、ルートウィンドウを引数として渡す
    root.mainloop() # Tkinterのイベントループを開始し、ウィンドウを表示する
