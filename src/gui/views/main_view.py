import tkinter as tk


from view import View
from "../controllers/main_view_controller" import MainViewController


class MainView(View):

    def __init__(self, parent):
        # set parent
        super().__init__(parent)
        self.parent = parent
        # set controller
        self.controller = self.init_controller()
        # init window and frames
        self.init_window()
        self.add_input_frame()
        self.add_fetch_frame()

    def init_window(self):
        # changing the title of our master widget
        self.parent.title("Projet Lisa")

        # allowing the widget to take the full space of the root window
        self.pack(fill=tk.BOTH, expand=1)

        # creating a menu instance
        menu = tk.Menu(self.parent)
        self.parent.config(menu=menu)

        # create the file object
        file = tk.Menu(menu)
        # add a command to file menu option
        file.add_command(label="Save")
        # add "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the edit object
        edit = tk.Menu(menu)
        # add a command to edit menu object
        # edit.add_command(label="Copy", command=self.showImg)
        # add "edit" to our menu
        menu.add_cascade(label="Edit", menu=edit)

        # create help object
        more = tk.Menu(menu)
        # add commands to help menu object
        more.add_command(label="Help")
        more.add_command(label="About")
        # add "more" to our Menu
        menu.add_cascade(label="More", menu=more)


    def init_controller(self):
        return MainViewController(self)


    def add_input_frame(self):
        self.input_frame = tk.Frame(self)

        tk.Label(self.input_frame, text="Input").grid(row=0)

        tk.Label(self.input_frame, text="Subject").grid(row=1)
        tk.Label(self.input_frame, text="Location").grid(row=2)
        self.subject = tk.Entry(self.input_frame)
        self.subject.grid(row=1, column=1)
        self.location = tk.Entry(self.input_frame)
        self.location.grid(row=2, column=1)

        tk.Label(self.input_frame, text="From").grid(row=1, column=2)
        tk.Label(self.input_frame, text="To").grid(row=2, column=2)

        self.date_start = tk.StringVar(value="2017-12-10")
        self.date_end = tk.StringVar(value="2017-12-10")
        tk.Button(self.input_frame, textvariable=self.date_start, command=lambda:self.controller.calendar_click(self.date_start)).grid(row=1, column=3)
        tk.Button(self.input_frame, textvariable=self.date_end, command=lambda:self.controller.calendar_click(self.date_end)).grid(row=2, column=3)

        tk.Button(self.input_frame, text="Fetch", command=self.controller.fetch).grid(row=3)

        self.input_frame.pack(fill="both", expand=True)
        self.input_frame.mainloop()


    def add_fetch_frame(self):
        fetch_frame = tk.Frame(self)
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
