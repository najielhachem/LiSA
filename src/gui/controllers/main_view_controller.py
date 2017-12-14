from .controller import Controller
from ..models.analyzer import Analyzer
import data_processing.parser as parser

import tkinter as tk
import tkcalendar
import tkinter.simpledialog as simpledialog
import data_processing.preprocessor as preprocessor
import time, datetime

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
        self.classifiers = self.load_classifiers()
    def load_classifiers(self, data_path = "../../../data"):
        """
        Function that return  a dictionary {name clf: trained clf} either by
        deserializing or retrain classifiers
        """
        #Load data_folder
        data = np.array(parser.read_json_folder())
        preprocessor.process_data(data[:,1])
        self.classifiers = get_classifiers()
        for key, value in self.classifiers.items():
            #if [key]need to train
            self.classifiers[key].fit(data[:,1], data[:,0])

    def init_model(self):
        self.model = Analyzer()

    def fetch(self):
        self.view.add_message(self.view.data_frame, "Fetching tweets...")
        self.view.rm_plot_frame()
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

    def analyze(self, name_clf="SVM"):
        # Classifie Tweets
        self.model.analyze(self.classifiers[name_clf])
        # Add Plot Frame
        self.view.add_plot_frame()
        self.view.btn_analyze.config(state='disabled')


    def plot(self):
        # get data
        period = int(self.view.period_entry.get())
        metric = self.view.period_metric.get()
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

        segemented_tweets = self.model.segment_labels(period, start, end)

        # plot data
        tweets = np.mean(segment_tweets, axis = 1)
        self.view.plot_data(tweets, np.arange(tweets.shape[0]))

    def calendar_click(self, var):
        cd = CalendarDialog(self.view)
        if cd.result != None:
            var.set(cd.result)
