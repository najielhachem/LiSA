from .controller import Controller
import data_processing.parser as parser

import tkinter as tk
import tkcalendar
import tkinter.simpledialog as simpledialog

class CalendarDialog(simpledialog.Dialog):
    """
    Dialog box that displays a calendar and returns the selected dat
    """
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
        subject = self.view.subject.get()
        location = self.view.location.get()
        tweets = parser.fetch_tweets(subject=subject, since=self.view.date_start.get(),
                        until=self.view.date_end.get(), near=(None if location == "" else location), limit=10)
        for tweet in tweets:
            print(tweet.text)
        self.view.add_analyse_frame()

    def calendar_click(self, var):
        cd = CalendarDialog(self.view)
        if cd.result != None:
            var.set(cd.result)
