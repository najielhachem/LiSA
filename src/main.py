import sys

import tkinter as tk

from gui.views.main_view import MainView

def main(argv):
    # root window created.
    root = tk.Tk()
    root.geometry("740x550")
    # add MainView to root
    MainView(root).pack(side="top", fill="both", expand=True)
    # main loop
    while True:
        try:
            root.mainloop()
            break
        except UnicodeDecodeError:
            pass


if __name__ == "__main__":
    main(sys.argv)
