from misc.modules import *
import plotly.graph_objs as go
import plotly.express as px
import datetime, os, json

with open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/misc/config.json') as f:
    chat_path = json.load(f)["chat.json path"]

def graph_mph():
    #-------RUN ONLY AFTER REFACTORING----------

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

    html_file = open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/res/htmls/mph.html', 'x')
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

    print(list(dates.values()))

    fig = px.line(
        x=list(dates.keys()),
        y=list(dates.values()),
        title='Mpd'
    )

    html_file = open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/res/htmls/mpd.html', 'x')
    html_file.truncate()
    fig.write_html(html_file, auto_open=False)
    html_file.close()

graph_mpd()