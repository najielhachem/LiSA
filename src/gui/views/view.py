from abc import ABC, abstractmethod

import tkinter as tk

class View(ABC, tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    @abstractmethod
    def init_controller(self):
        pass
