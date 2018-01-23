from .controller import Controller
from ..models.analyzer import Analyzer
import gui.models.classifiers as classifier
import data_processing.parser as parser
from tkinter import filedialog
import numpy as np

import tkinter as tk
import tkcalendar
import tkinter.simpledialog as simpledialog
import data_processing.preprocessor as preprocessor
import time, datetime

from ..models.fetchThread import FuncThread

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

    def init_model(self, clfname = "SVM"):
        clf = classifier.get_classifiers()[clfname]
        self.model = Analyzer(clf)

    def fetchThread(self):
        self.view.add_message(self.view.data_frame, "Fetching tweets...")
        self.view.rm_plot_frame()
        self.view.update()
        subject = self.view.subject.get()
        location = self.view.location.get()
        limit = int(self.view.limit.get())
        since = self.view.date_start.get()
        until = self.view.date_end.get()
        tweets = parser.fetch_and_save_tweets(filename=subject + '.json', subject=subject, since=since, until=until, near=(None if location == "" else location), limit=limit)
        print('Tweets returned  : ' + str(len(tweets)))
        self.model.set_tweets(tweets)
        text_message = "Tweets that match your requirements are downloaded and ready to be to be proceseed!\nTotal of {} tweets download".format(len(tweets))
        self.view.add_message(self.view.data_frame, text_message)
        self.view.btn_analyze.config(state='normal')

    def export(self):
        #check if something is fetched
        if (self.model.get_tweets() == []):
            self.fetch()
        tweets = self.model.get_tweets()
        #opend a dialog boxe
        f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if not(f == None):
            parser.save_tweets_2_file(tweets, f)
            f.close()

    def fetch(self):
        self.f = FuncThread(self.fetchThread)
        self.f.start()
        self.view.addProgressBar()

    def cancel(self):
        self.f = None

    def analyze(self):
        self.view.add_message(self.view.data_frame, "Analyzing tweets")
        self.view.update()
        # Classifie Tweets
        self.model.analyze()
        self.view.add_message(self.view.data_frame, "Tweet analyzed")
        self.view.update()
        # Add Plot Frame
        self.view.add_plot_frame()
        self.view.btn_analyze.config(state='disabled')


    def plot(self):
        # get data
        period = int(self.view.period_entry.get())
        metric = self.view.period_metric.get()
        if metric == 'minutes':
            period *= 60
        if metric == 'hours':
            period *= 3600
        if metric == 'days':
            period *= 3600 * 24
        if metric == 'months':
            period *= 3600 * 24 * 30

        # divide Tweets based on timestamp and period
        start = self.view.date_start.get()
        start = time.mktime(datetime.datetime.strptime(start, "%Y-%m-%d").timetuple())
        end = self.view.date_end.get()
        end = time.mktime(datetime.datetime.strptime(end, "%Y-%m-%d").timetuple())

        # get data
        evaluations, periods = self.model.segment_labels(period, start, end)

        # truncate data_frame
        n = evaluations.shape[0]
        i0, i1 = -1, -1
        for i in range(n):
            if evaluations[i] != -2 and i0 == -1:
                i0 = i
            if evaluations[n - i - 1] != -2 and i1 == -1:
                i1 = n - i

        periods = periods[i0:i1]
        evaluations = evaluations[i0:i1]
        empty_idx = np.where(evaluations == -2)[0]
        pos_idx = np.where(evaluations > 0)[0]
        neg_idx = np.where((evaluations < 0) & (evaluations != -2))[0]
        ticks = np.arange(i0, i1)

        # plot data
        self.view.plot_data(pos_idx, neg_idx, empty_idx, evaluations, ticks, periods)

    def calendar_click(self, var):
        cd = CalendarDialog(self.view)
        if cd.result != None:
            var.set(cd.result)
