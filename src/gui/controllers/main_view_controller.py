from .controller import Controller
import data_processing.parser as parser

import tkinter as tk
import tkcalendar
import tkinter.simpledialog as simpledialog

class CalendarDialog(simpledialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = tkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection_get()

class MainViewController(Controller):

    def __init__(self, view):
        self.view = view

    def fetch(self):
        text = "Fetching tweets..."
        tk.Label(self.view.input_frame, text=text).grid(row=4)
        self.view.input_frame.update()
        tweets = parser.fetch_tweets(subject=self.view.subject.get(), since=self.view.date_start.get(),
                        until=self.view.date_end.get(), near=self.view.location.get())
        print(tweets)

    def calendar_click(self, var):
        cd = CalendarDialog(self.view)
        var.set(cd.result)
