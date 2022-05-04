import json
import datetime

def standarize_stat(line):
    if line == '' or not ('.' in line or '/' in line) or not ':' in line or not line[0] in "0987654321":
        return None

    if not len([True for x in line[:11] if x in "1234567890/.,: "]) == 11:
        return None

    i = 0
    while line[i] not in [".", "/"]:
        i += 1

    raw = line[line.find(" - ") + 3:line.find("\n")]
    user = raw[:raw.find(':')]
    text = raw[raw.find(':') + 2:]

    if line[line.find(" - ") - 2:line.find(" - ")] == "PM":
        hour = int(line[line.find(" "):line.find(":")]) + 12
        minute = int(line[line.find(":") + 1:line.find(" PM")])

    elif line[line.find(" - ") - 2:line.find(" - ")] == "AM":
        hour = int(line[line.find(" "):line.find(":")])
        minute = int(line[line.find(":") + 1:line.find(" AM")])
    else:
        minute = line[line.find(" - ") - 2:line.find(" - ")]
        hour = line[line.find(" - ") - 5:line.find(" - ") - 3]

    if hour == 24:
        hour = 0

    if line[i] == ".":
        day = line[:i]
        line = line[i + 1:]
        i = line.find(".")
        month = line[:i]
        year = line[i + 1:line.find(",")]
    else:
        month = line[:i]
        line = line[i + 1:]
        i = line.find("/")
        day = line[:i]
        year = line[i + 1:line.find(",")]

    if len(str(year)) == 2:
        year = "20" + str(year)

    #print([True for x in line[:11] if (x in "1234567890/.,: ") and bool(x)], line[:11])
    return [int(year), int(month), int(day), int(hour), int(minute), user, text]

def add_line(line, mass):
    stats = standarize_stat(line)
    if not stats:
        return

    d = {}

    d["time"] = list(datetime.datetime(stats[0], stats[1], stats[2], stats[3], stats[4]).timetuple())
    #d["time"] = list(datetime.datetime.now().timetuple())
    d["text"] = stats[-1]
    d["user"] = stats[-2]
    d["app"] = "wa"

    mass.append(d)
    print("committed ", line)

messages = []

with open(input(), 'r') as f:
    for line in f:
        add_line(line, messages)

with open("../res/chat.json", 'r') as f:
    d = json.load(f)

for message in messages:
    d["messages"].append(message)

with open("../res/chat.json", 'w') as f:
    json.dump(d, f)
