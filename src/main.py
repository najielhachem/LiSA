import sys

import tkinter as tk

from gui.views.main_view import MainView

def main(argv):
    # root window created.
    root = tk.Tk()
    root.geometry("400x300")
    # add MainView to root
    MainView(root).pack(side="top", fill="both", expand=True)
    # main loop
    root.mainloop()


if __name__ == "__main__":
    main(sys.argv)
