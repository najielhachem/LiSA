from abc import ABC, abstractmethod

import tkinter as tk

class View(ABC, tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    @abstractmethod
    def init_controller(self):
        pass
