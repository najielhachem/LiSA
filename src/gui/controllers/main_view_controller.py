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

import threading

from ..models.fetchThread import FuncThread, ctype_async_raise

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
        self.stopped = False

    def init_model(self, clfname = "SVM"):
        clf = classifier.get_classifiers()[clfname]
        self.model = Analyzer(clf)

    def fetchThread(self):
        self.view.add_message(self.view.data_frame, "Fetching tweets...")
        self.view.rm_analyze_frame()
        self.view.update()
        subject = self.view.subject.get()
        location = self.view.location.get()
        limit = int(self.view.limit.get())
        since = self.view.date_start.get()
        until = self.view.date_end.get()

        if not self.view.chk_cache.get():
            print("no caching")
            tweets = parser.fetch_tweets(subject=subject, since=since,
                        until=until, near=(None if location == "" else location),
                        limit=limit)
        else :
            print("caching")
            tweets = parser.fetch_and_save_tweets(filename=subject + '.json',
                    subject=subject, since=since, until=until,
                    near=(None if location == "" else location), limit=limit)
        
        if (self.stopped):
            self.stopped = False
            self.fetch_thread = None
            return
 
        self.model.set_tweets(tweets)
        
        text_message = "Tweets that match your requirements are downloaded and ready to be to be proceseed!\nTotal of {} tweets download".format(len(tweets))
        self.view.add_message(self.view.data_frame, text_message)
        
        self.view.btn_analyze.config(state='normal')
        self.view.btn_save.config(state='normal')
        self.fetch_thread = None

    def load(self):
        #opend a dialog boxe
        filepath = filedialog.askopenfilename(filetypes=[("Json Files", "*.json")])
        if filepath:
            try:
                query, tweets = parser.read_tweets(filepath)
                self.model.set_tweets(tweets)
                self.view.subject.delete(0, 'end')
                self.view.subject.insert('end', query['subject'])
                self.view.location.delete(0, 'end')
                self.view.location.insert('end', query['near'])
                self.view.limit.delete(0, 'end')
                self.view.limit.insert('end', str(tweets.shape[0]))
                self.view.date_start.set(query['since'])
                self.view.date_end.set(query['until'])
                self.view.btn_analyze.config(state='normal')
                self.view.btn_save.config(state='normal')
            except Exception as ex:
                tk.messagebox.showerror("Loading Error", ex)


    def save(self):
        tweets = self.model.get_tweets()
        
        #opend a dialog boxe
        f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if f:
            subject = self.view.subject.get()
            near = self.view.location.get()
            since = self.view.date_start.get()
            until = self.view.date_end.get()
            parser.save_tweets(f, subject, near, since, until, tweets)

    def fetch(self):
        self.fetch_thread = threading.Thread(target=self.fetchThread)
        self.fetch_thread.start()

    def cancel(self):
        if (self.fetch_thread != None):
            self.stopped = True
            ctype_async_raise(self.fetch_thread, SystemExit)
            self.view.remove_message()

    def analyze(self):
        self.view.add_message(self.view.data_frame, "Analyzing tweets")
        self.view.update()
 
        # Classifie Tweets
        self.model.analyze()
        self.view.add_message(self.view.data_frame, "Tweet analyzed")
        self.view.update()
        
        # Add Analyze Frame
        self.view.add_analyze_frame()
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
        end += 3600 * 24 

        # get data
        evaluations, periods = self.model.segment_labels(period, start, end)
        
        n = evaluations.shape[0]
        i0, i1 = 0, n
        
        # truncate data_frame
        if self.view.chk_trim.get():
            for i in range(n):
                if evaluations[i] != -2 and i0 == 0:
                    i0 = i
                if evaluations[n - i - 1] != -2 and i1 == n:
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
