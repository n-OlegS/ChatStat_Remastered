from misc.d_modules import *
from collections import defaultdict
import plotly.graph_objs as go
import plotly.express as px
from scipy import signal
import datetime, json #, os,

sign = ''

CONFIGPATH = "/Users/oleg/PycharmProjects/chatstat_remastered/misc/config.json"
HTML_DIR = "/Users/oleg/PycharmProjects/chatstat_remastered/res/htmls/"

with open(CONFIGPATH) as f:
    chat_path = json.load(f)["chat.json path"]


def graph_mph():
    # -------RUN ONLY AFTER REFACTORING----------

    with open(chat_path) as f:
        d = json.load(f)["messages"]

    users = {}
    data = []

    for elem in d:
        user = elem["user"]
        if user not in users:
            users[user] = {}
            for i in range(24):
                users[user][str(i)] = 0

        hour = str(elem["time"][3])
        users[user][hour] += 1

    base = [0] * 24

    for i in list(users.keys()):
        data.append(go.Bar(
            name=i,
            x=list(users[i].keys()),
            y=list(users[i].values()),
            base=base,
            offsetgroup=0
        ))

        base = addLists(base, list(users[i].values()))

    fig = go.Figure(
        data,
        layout=go.Layout(
            title="Messages per hour of day",
            yaxis_title="Number of messages"
        )
    )

    html_file = open(f'{HTML_DIR}mph.html', 'x')
    html_file.truncate()
    fig.write_html(html_file, auto_open=False)
    html_file.close()


def graph_mpd():
    with open(chat_path) as f:
        d = json.load(f)["messages"]
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

    html_file = open(f'{HTML_DIR}mpd.html', 'x')
    html_file.truncate()
    fig.write_html(html_file, auto_open=False)
    html_file.close()


def graph_mpd_v2():
    with open(chat_path) as f:
        d = json.load(f)["messages"]
    dates = {}

    for mess in d:
        date = mess["time"][:3]

        if '-'.join([str(x) for x in date]) not in list(dates.keys()):
            dates['-'.join([str(x) for x in date])] = 1
        else:
            dates['-'.join([str(x) for x in date])] += 1

    print([x for x in list(set(list(dates.keys()))) if not isinstance(x, int)])

    fig = px.line(
        x=list(dates.keys()),
        y=list(signal.savgol_filter([x for x in list(dates.values()) if 0 <= x <= 50000], 200, 3)),
    )

    html_file = open(f'{HTML_DIR}mpdv2.html', 'x')
    html_file.truncate()
    fig.write_html(html_file, auto_open=False)
    html_file.close()


def better_parse(req, st):
    if req[0] == '(':
        req = req[1:-1]

    if not ("+" in req or "*" in req):
        return (req in st)

    else:
        if '(' in req:
            req_res = req[:req.find('(')]
        else:
            req_res = req

        if "+" in req_res:
            type = '+'
        else:
            type = '*'

    connections = []
    for elem in req.split(type):
        connections.append(better_parse(elem, st))

    if (type == '+' and (connections[0] or connections[1])) or (type == "*" and (connections[0] and connections[1])):
        return 1
    else:
        return 0

"""
def graph_worduse(word):
    count = 0
    with open(chat_path) as f:
        d = json.load(f)["messages"]

    dates = {}

    for mess in d:
        date = mess["time"][:3]

        # if word in [''.join(y for y in x.lower() if y.isalpha()) for x in mess["text"].split()]:
        if better_parse(word, ' '.join([''.join(y for y in x.lower() if y.isalpha()) for x in mess["text"].split()])):
            count += 1
            if '-'.join([str(x) for x in date]) not in list(dates.keys()):
                dates['-'.join([str(x) for x in date])] = 1
            else:
                dates['-'.join([str(x) for x in date])] += 1

    print(dates)

    fig = px.bar(
        x=list(dates.keys()),
        y=list(dates.values()),
    )

    html_file = open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/res/htmls/wug.html', 'x')
    html_file.truncate()
    fig.write_html(html_file, auto_open=False)
    html_file.close()


def graph_activity():
    count = 0
    with open(chat_path) as f:
        d = json.load(f)["messages"]

    with open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/misc/config.json') as f:
        u1, u2 = list(json.load(f)["aliases"].keys())
        print(u1, u2)
    dates = {}
    current_date = 0

    user1 = set()

    for mess in d:
        date = mess["time"][:3]
        date = '-'.join([str(x) for x in date])
        user = mess["user"]

        if user not in [u1, u2]:
            print("USER EXCEPTION:", user)

        if current_date == 0:
            current_date = date

        if date != current_date:
            try:
                dates[current_date] = dates[current_date][u1] / (dates[current_date][u1] + dates[current_date][u2])
            except Exception:
                print("??")
            user1.add(u1)
            current_date = date

        if date not in dates:
            dates[date] = defaultdict()
            dates[date].default_factory = lambda: 0

        try:
            if user in dates[date]:
                dates[date][user] += 1
            else:
                dates[date][user] = 1
        except Exception:
            try:
                print(user, dates[date])
            except Exception:
                pass
            continue

    print(dates, "\n", user1)

    fig = px.bar(
        x=list(dates.keys()),
        y=list(dates.values()),
    )

    html_file = open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/res/htmls/ag.html', 'x')
    html_file.truncate()
    fig.write_html(html_file, auto_open=False)
    html_file.close()


def graph_activity_v2():
    count = 0
    with open(chat_path) as f:
        d = json.load(f)["messages"]

    with open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/misc/config.json') as f:
        u1, u2 = list(json.load(f)["aliases"].keys())
        print(u1, u2)
    dates = {}
    current_date = 0

    user1 = set()

    for mess in d:
        date = mess["time"][:3]
        date = '-'.join([str(x) for x in date])
        user = mess["user"]

        if user not in [u1, u2]:
            print("USER EXCEPTION:", user)

        if current_date == 0:
            current_date = date

        if date != current_date:
            try:
                dates[current_date] = dates[current_date][u1] / (dates[current_date][u1] + dates[current_date][u2])
            except Exception:
                print("??")
            user1.add(u1)
            current_date = date

        if date not in dates:
            dates[date] = defaultdict()
            dates[date].default_factory = lambda: 0

        try:
            if user in dates[date]:
                dates[date][user] += 1
            else:
                dates[date][user] = 1
        except Exception:
            try:
                print(user, dates[date])
            except Exception:
                pass
            continue

    print(dates, "\n", user1)

    fig = go.Figure

    fig.add_trace(go.Scatter(
        x=[x for x in list(dates.keys()) if isinstance(x, str)],
        y=signal.savgol_filter([x for x in list(dates.values()) if isinstance(x, float)], 53, 7),
        mode='markers',
        marker=dict(
            size=6,
            color='mediumpurple',
            symbol='triangle-up'
        ),
        name='Activity',
    ))


    fig.show()
"""
graph_mpd()
graph_mpd_v2()
#graph_worduse("a*(b+c)")

