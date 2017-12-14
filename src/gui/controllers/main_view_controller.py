from .controller import Controller
from ..models.analyzer import Analyzer
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
        self.init_model()

    def init_model(self):
        self.model = Analyzer()

    def fetch(self):
        self.view.add_message(self.view.data_frame, "Fetching tweets...")
        subject = self.view.subject.get()
        location = self.view.location.get()
        limit = int(self.view.limit.get())
        since = self.view.date_start.get()
        until = self.view.date_end.get()
        tweets = parser.fetch_tweets(subject=subject, since=since,
                        until=until, near=(None if location == "" else location), limit=limit)
        self.model.set_tweets(tweets)
        self.view.add_message(self.view.data_frame, "Tweets that match your requirements are downloaded and ready to be to be proceseed!")
        self.view.btn_analyze.config(state='normal')

    def analyze(self):
        # Classifie Tweets
        #### # self.model.analyze()
        # Add Plot Frame
        self.view.add_plot_frame()


    def plot(self):
        # divide Tweets based on timestamp and period

        # plot data
        tweets = [1,2,3,4,5,6,7,8] # for testing
        periods = [5,6,1,3,8,9,3,5] # for testing
        self.view.plot_data(tweets, periods)

    def calendar_click(self, var):
        cd = CalendarDialog(self.view)
        if cd.result != None:
            var.set(cd.result)
