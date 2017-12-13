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
        self.view.add_start_fetch_message()
        subject = self.view.subject.get()
        location = self.view.location.get()
        limit = int(self.view.limit.get())
        since = self.view.date_start.get()
        until = self.view.date_end.get()
        tweets = parser.fetch_tweets(subject=subject, since=since,
                        until=until, near=(None if location == "" else location), limit=limit)
        self.view.add_end_fetch_message()

    def calendar_click(self, var):
        cd = CalendarDialog(self.view)
        if cd.result != None:
            var.set(cd.result)
