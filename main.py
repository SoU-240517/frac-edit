# julia_viewer/main.py
import tkinter as tk
from ui.main_window import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root) # MainWindowクラスをインスタンス化
    root.mainloop()
