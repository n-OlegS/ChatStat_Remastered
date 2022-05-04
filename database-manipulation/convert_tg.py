import json, datetime
from modules import standartize_tg

def generate_tg(path):
    def add_line(mess, mass):
        stats = standartize_tg(mess)
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

    with open(path, 'r') as f:
        orig = json.load(f)
        for elem in orig["messages"]:
            add_line(elem, messages)

    d = {"messages" : []}

    for message in messages:
        d["messages"].append(message)

    return d


with open("./res/chat.json", 'w') as f:
    json.dump(generate_tg(input()), f)

