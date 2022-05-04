import json, datetime

def standartize(mess):
    if type(mess["text"]) != str or not bool(mess["text"]):
        return

    user = mess["from"]
    text = mess["text"]

    time = datetime.datetime.strptime(mess["date"], "%Y-%m-%dT%H:%M:%S")

    return [time, user, text]

def add_line(mess, mass):
    stats = standartize(mess)
    if not stats:
        return

    d = {}

    d["time"] = stats[0].timetuple()
    d["text"] = stats[-1]
    d["user"] = stats[-2]
    d["app"] = "tg"

    mass.append(d)
    print("committed ", stats[-1])

messages = []

with open(input(), 'r') as f:
    orig = json.load(f)
    for elem in orig["messages"]:
        add_line(elem, messages)

with open("res/chat.json", 'r') as f:
    d = json.load(f)

for message in messages:
    d["messages"].append(message)

with open("res/chat.json", 'w') as f:
    json.dump(d, f)

