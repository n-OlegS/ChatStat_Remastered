import json, datetime
from modules import standartize_wa


def generate_wa(path):
    def add_line(line, mass):
        stats = standartize_wa(line)
        if not stats:
            return

        d = {}

        d["time"] = list(datetime.datetime(stats[0], stats[1], stats[2], stats[3], stats[4]).timetuple())
        # d["time"] = list(datetime.datetime.now().timetuple())
        d["text"] = stats[-1]
        d["user"] = stats[-2]
        d["app"] = "wa"

        mass.append(d)
        print("committed ", line)


    messages = []

    with open(path, 'r') as f:
        for line in f:
            add_line(line, messages)

    d = {"messages" : []}

    for message in messages:
        d["messages"].append(message)

    return d

with open("./res/chat.json", 'w') as f:
    json.dump(generate_wa(input()), f)
