import sys

import tkinter as tk

from gui.views.main_view import MainView

def main(argv):
    root = tk.Tk()
    MainView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main(sys.argv)
