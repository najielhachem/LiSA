import tkinter as tk

from .view import View
from ..controllers.main_view_controller import MainViewController

class MainView(View):

    def __init__(self, parent, *args, **kwargs):
        self.controller = self.init_controller()
        self.add_input_frame()
        super(MainView, self).__init__(parent, *args, **kwargs)


    def init_controller(self):
        return MainViewController(self)

    def add_input_frame(self):
        input_frame = tk.Frame(self)
        btn_fetch = tk.Button(input_frame, text="fetch", command=self.controller.fetch)
        pass

    def add_fetch_frame(self):
        fetch_frame = tk.frame(self)
        pass

    def add_plot_frame(self):
        pass


# root = Tk()
# root.title('Lisa')
# root['bg']='white'
#
#
# # frame 1
# inputFrame = Frame(root, borderwidth=2)
# inputFrame.pack(side=TOP, padx=10, pady=10)
#
# for line, item in enumerate(['input', 'suject', 'Location']):
#     l = Label(inputFrame, text=item, width=10)
#     e = Entry(inputFrame, width=10)
#     l.grid(row=line, column=0)
#     e.grid(row=line, column=1)
# Label(inputFrame, text='DatePicker', width=10).grid(row=1, column = 2)
#
# dp.Datepicker(inputFrame).grid(row = 0, column = 3)
# dp.Datepicker(inputFrame).grid(row = 2, column = 3)
#
#
# OptionFrame = Frame(root, borderwidth=2, relief=GROOVE)
# OptionFrame.pack(side=TOP, padx=10, pady=10)
#
# PlotFrame = Frame(root, borderwidth=2, relief=GROOVE)
# PlotFrame.pack(side=TOP, padx=10, pady=10)
#
#
#
# root.mainloop()
