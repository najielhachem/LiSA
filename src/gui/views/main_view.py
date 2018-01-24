import tkinter as tk
import datetime
import gui.models.classifiers as classifier
from ..models.analyzer import Analyzer
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from .view import View
from ..controllers.main_view_controller import MainViewController
from tkinter.ttk import Progressbar
from tkinter import HORIZONTAL

class MainView(View):

    def __init__(self, parent):
        # set parent
        super().__init__(parent)
        self.parent = parent
        # set controller
        self.controller = self.init_controller()
        # init window and frames
        self.init_window()
        self.add_data_frame()
        # Setting Reusable Variables to None
        self.analyze_frame = None
        self.toolbar_frame = None
        self.message_box = None

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

    def add_data_frame(self):
        self.data_frame = tk.Frame(self)
        self.data_frame.grid(row=0, column=0, sticky='ne', padx=10)
        # Frame title
        lbl_frame = tk.Label(self.data_frame, text="Fetcher")
        lbl_frame.grid(row=0, column=0, columnspan=2, pady=20)
        lbl_frame.config(font=("Courier", 20))
        self.add_input_form(self.data_frame)

    def add_analyze_frame(self):
        self.analyze_frame = tk.Frame(self)
        self.analyze_frame.grid(row=0, column=1, padx=10, sticky='n')
        # Frame title
        lbl_frame = tk.Label(self.analyze_frame, text="Analyzer")
        lbl_frame.grid(row=0, column=0, columnspan=3, pady=20)
        lbl_frame.config(font=("Courier", 20))
        self.add_plot_frame(self.analyze_frame)

    def rm_analyze_frame(self):
        if self.analyze_frame is not None:
            self.analyze_frame.grid_forget()

    def add_plot_frame(self, frame):
        # Period Label
        self.plot_frame = tk.Frame(frame, bd=10, relief='raised')
        self.plot_frame.grid(row=1, column=0, columnspan=3, ipadx=5, ipady=5)
        lbl_period = tk.Label(self.plot_frame, text='Period')
        lbl_period.grid(row=1, column=0, padx=(10, 0))

        # Period Entry
        self.period_entry = tk.Entry(self.plot_frame)
        self.period_entry.insert('end', '10')
        self.period_entry.grid(row=1, column=1)

        # Period Metric
        self.period_metric = tk.StringVar(self.plot_frame)
        self.period_metric.set('hours')
        opt_metric = tk.OptionMenu(self.plot_frame, self.period_metric,
                "seconds", "minutes", "hours", "days", "months")
        opt_metric.grid(row=1, column=2)

        # Add Trim Check Box
        self.chk_trim = tk.IntVar()
        self.btn_trim = tk.Checkbutton(self.plot_frame, text='Trim Data',
                variable=self.chk_trim)
        self.btn_trim.toggle()
        self.btn_trim.grid(row=2, column=0, columnspan=2, stick='e')

        # Plot Button
        btn_plot = tk.Button(self.plot_frame, text='Plot',
                command=self.controller.plot)
        btn_plot.grid(row=2, column=2, sticky='we')

    def add_input_form(self, frame):
        input_frame = tk.Frame(frame, bd=10, relief='sunken')
        input_frame.grid(row=1, column=0, columnspan=2, ipadx=5, ipady=5)

        # Subject Input
        tk.Label(input_frame, text="Subject").grid(row=1, column=0, pady=(10,0))
        self.subject = tk.Entry(input_frame)
        self.subject.insert('end', 'Trump')
        self.subject.grid(row=1, column=1, pady=(10,0))

        # Location Input
        tk.Label(input_frame, text="Location").grid(row=2, column=0)
        self.location = tk.Entry(input_frame)
        self.location.insert('end', 'Paris')
        self.location.grid(row=2, column=1)

        # Number of Tweets Input
        tk.Label(input_frame, text="Nb Tweets").grid(row=3, column=0)
        self.limit = tk.Entry(input_frame)
        self.limit.insert('end', '10')
        self.limit.grid(row=3, column=1)

        # Start date interval
        number_days_offset = 7
        # Current date
        now = datetime.datetime.now()
        begin = now - datetime.timedelta(days=number_days_offset)

        # Start Date Input
        tk.Label(input_frame, text="From").grid(row=4, column=0)
        self.date_start = tk.StringVar(value = str(begin.year) + "-"
                + str(begin.month) + "-" + str(begin.day))
        btn_start = tk.Button(input_frame, textvariable=self.date_start,
                command=lambda:self.controller.calendar_click(self.date_start))
        btn_start.grid(row=4, column=1, sticky='we')

        # End Date Input
        tk.Label(input_frame, text="To").grid(row=5, column=0)
        self.date_end = tk.StringVar(value=str(now.year) + "-"
                + str(now.month) + "-" + str(now.day))
        btn_end = tk.Button(input_frame, textvariable=self.date_end,
                command=lambda:self.controller.calendar_click(self.date_end))
        btn_end.grid(row=5, column=1, sticky='we')

        # Add seperator
        sep_frame = tk.Frame(frame, bd=3, relief='groove', height=10, bg='black')
        sep_frame.grid(row=2, column=0, columnspan=2, sticky='we', pady=(0, 0))

        # Buttons subframe
        btn_frame = tk.Frame(frame, bd=10, relief='sunken')
        btn_frame.grid(row=3, column=0, columnspan=2, ipadx=5, ipady=5)

        # Add Fetch Tweets Button
        self.btn_fetch = tk.Button(btn_frame, text="Fetch Tweets",
                command=self.controller.fetch)
        self.btn_fetch.grid(row=0, column=0, sticky='e', pady=(10,0), padx=(10, 0))

        # Add Cancel Fetch Tweets Button
        self.btn_fetch = tk.Button(btn_frame, text="Cancel Fetch",
                command=self.controller.cancel)
        self.btn_fetch.grid(row=0, column=1, sticky='w', pady=(10,0))

        # Add Load Tweets Button
        self.btn_load = tk.Button(btn_frame, text="Load Tweets",
                command=self.controller.load)
        self.btn_load.grid(row=1, column=0, sticky='e')

        # Add export Tweets Button
        self.btn_save = tk.Button(btn_frame, text="Save Tweets",
                command=self.controller.save)
        self.btn_save.grid(row=1, column = 1, sticky='w')
        self.btn_save.config(state='disabled')

        # Add Save Tweets Check Box
        self.chk_cache = tk.IntVar()
        self.btn_cache = tk.Checkbutton(btn_frame, text='Use Cache',
                variable=self.chk_cache)
        self.btn_cache.toggle()
        self.btn_cache.grid(row=3, column=0, columnspan=2)

        # Add choose classifier Button
        self.btn_choose_clf = tk.Button(btn_frame, text="Advanced",
                command= self.popup_list_clf)
        self.btn_choose_clf.grid(row=4, column = 0, columnspan=2,
                pady=(15,0))

        # Add Analyze Tweets Button
        self.btn_analyze = tk.Button(btn_frame, text="Analyze Tweets",
                command=self.controller.analyze)
        self.btn_analyze.grid(row=5, column=0, columnspan=2)
        self.btn_analyze.config(state='disabled')

    def add_message(self, frame, msg):
        if self.message_box is None:
            self.message_box = tk.Message(frame, text=msg, relief='raised', aspect=400, bd=5, width=250)
            self.message_box.grid(row=4, column=0, columnspan=2, pady=10)
        else:
            self.message_box.config(text=msg)

    def remove_message(self):
        if self.message_box != None:
            self.message_box.destroy()
            self.message_box = None

    def popup_list_clf(self):
        win = tk.Toplevel()
        win.wm_title("Choose Classifiers")
        listbox = tk.Listbox(win)
        listbox.pack()
        clfs = classifier.get_classifiers()
        value = None
        for key, value in clfs.items():
            listbox.insert(tk.END, key)
        b = tk.Button(win, text="validate", command = lambda: [f() for f in [lambda:self.controller.init_model(listbox.get(tk.ACTIVE)),win.destroy]])
        b.pack()

    def plot_data(self, pos_idx, neg_idx, empty_idx,
            evaluations, ticks, periods):
        #init a figure
        fig = Figure(figsize=(4,4), dpi=80)
        ax = fig.add_subplot(111)

        # plot middle line
        ax.axhline(c='c', ls='-')
        # plot empty periods
        emp, = ax.plot(empty_idx + ticks[0], [0] * empty_idx.shape[0], 'kX')
        # plot positive periods
        pos = ax.bar(pos_idx + ticks[0], evaluations[pos_idx], color= 'g')
        # plot negative periods
        neg = ax.bar(neg_idx + ticks[0], evaluations[neg_idx], color= 'r')

        # set axes parameters
        ax.set_ylim([-1.5, 1.5])
        ax.set_xticklabels(["T {}".format(t) for t in ticks],
                rotation='vertical', fontsize=7)
        ax.set_xlabel('Period')
        ax.set_ylabel('Average Period Polarity')

        # show legend
        handles, labels = [], []
        if empty_idx.shape[0] != 0:
            handles.append(emp)
            labels.append("Empty")
        if pos_idx.shape[0] != 0:
            handles.append(pos[0])
            labels.append("Positive")
        if neg_idx.shape[0] != 0:
            handles.append(neg[0])
            labels.append("Negative")
        ax.legend(handles, labels, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)

        # aggregate the figure to the frame plot
        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.show()
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=3)

        # adding the toolbar to the frame plot
        if self.toolbar_frame is not None:
            self.toolbar_frame.destroy()
        self.toolbar_frame = tk.Frame(self.plot_frame)
        self.toolbar_frame.grid(row=4, column=0, columnspan=3, rowspan=2, sticky='w')
        toolbar = NavigationToolbar(canvas, self.toolbar_frame)
        toolbar.pack(side='left')
        toolbar.update()

        # setting values under cursor
        def __format_coord(x, y):
            if toolbar._active is not None:
                return ""
            col = int(x+0.5)
            if ticks.shape[0] == 1:
                return ''
            if col >= ticks[0] and col <= ticks[-1]:
                T1, T2 = periods[col - ticks[0]]
                if T1 is None:
                    return 'No tweets'
                return 'From: {}\nTo   : {}'.format(T1, T2)
            return 'No tweets'
        ax.format_coord = __format_coord


class NavigationToolbar(NavigationToolbar2TkAgg):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2TkAgg.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom')]
