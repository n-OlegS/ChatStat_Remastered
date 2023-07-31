import json
import time
import datetime
from misc.d_modules import *
from collections import defaultdict
import plotly.graph_objs as go
import plotly.express as px
from scipy import signal
import datetime, os


class Modules:
    def __init__(self):
        with open('config.json', 'r') as f:
            chat_dir = json.load(f)["chat dir"]

        chatf = []
        i = 0

        while 1:
            try:
                with open(f"{chat_dir}{i}.json", 'r') as c:
                    chatf += json.load(c)["messages"]
                    i += 1

            except FileNotFoundError:
                print("Broken,", i)
                break

        self.chatf = chatf

    def get_hours(self):
        d = self.chatf

        last_time = datetime.datetime.min
        minutes = []

        count = 0

        for mess in d:
            if len(minutes) == 100:
                del minutes[0]

            current_time = datetime.datetime.fromtimestamp(time.mktime(tuple(mess["time"])))
            delta = current_time - last_time

            time_tuple = list(current_time.timetuple())[:5]

            if delta.seconds < 120 and time_tuple not in minutes:
                minutes.append(time_tuple)
                count += 1

            last_time = current_time

        return count

    def graph_mpd(self):
        d = self.chatf
        dates = {}

        for mess in d:
            date = mess["time"][:3]

            if '-'.join([str(x) for x in date]) not in list(dates.keys()):
                dates['-'.join([str(x) for x in date])] = 1
            else:
                dates['-'.join([str(x) for x in date])] += 1

        fig = px.line(
            x=list(dates.keys()),
            y=list(dates.values()),
        )

        html_file = open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/res/htmls/mpd.html', 'x')
        html_file.truncate()
        fig.write_html(html_file, auto_open=False)
        html_file.close()

    def graph_mpd_v2(self):
        d = self.chatf
        dates = {}

        for mess in d:
            date = mess["time"][:3]

            if '-'.join([str(x) for x in date]) not in list(dates.keys()):
                dates['-'.join([str(x) for x in date])] = 1
            else:
                dates['-'.join([str(x) for x in date])] += 1

        fig = px.line(
            x=list(dates.keys()),
            y=list(signal.savgol_filter([x for x in list(dates.values()) if 0 <= x <= 50000 and isinstance(x, int)], len(dates),
                                        40)),
        )

        html_file = open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/res/htmls/mpd.html', 'x')
        html_file.truncate()
        fig.write_html(html_file, auto_open=False)
        html_file.close()


modules = Modules()
print("Minutes spent in chat: ", modules.get_hours())

