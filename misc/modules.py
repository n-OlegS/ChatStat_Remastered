import datetime, json, os, time

with open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/misc/config.json') as f:
    chat_path = json.load(f)["chat.json path"]

def standartize_wa(line):
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

def standartize_tg(mess):
    if type(mess["text"]) != str or not bool(mess["text"]):
        return

    user = mess["from"]
    text = mess["text"]

    time = datetime.datetime.strptime(mess["date"], "%Y-%m-%dT%H:%M:%S")

    return [time, user, text]

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
        #print("committed ", stats[-1])

    messages = []

    with open(path, 'r') as f:
        orig = json.load(f)
        for elem in orig["messages"]:
            add_line(elem, messages)

    d = {"messages" : []}

    for message in messages:
        d["messages"].append(message)

    return d

def generate_wa(path):
    def add_line(line, mass):
        stats = standartize_wa(line)
        if not stats:
            return

        d = {}

        d["time"] = datetime.datetime(stats[0], stats[1], stats[2], stats[3], stats[4]).timetuple()
        # d["time"] = list(datetime.datetime.now().timetuple())
        d["text"] = stats[-1]
        d["user"] = stats[-2]
        d["app"] = "wa"

        mass.append(d)
        #print("committed ", line)


    messages = []

    with open(path, 'r') as f:
        for line in f:
            add_line(line, messages)

    d = {"messages" : []}

    for message in messages:
        d["messages"].append(message)

    return d


def refactor_database():
    with open(chat_path) as f:
        d = json.load(f)["messages"]

    with open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/misc/config.json') as f:
        aliases = json.load(f)["aliases"]

    for elem in d:
        name = elem["user"]

        for i in range(len(aliases)):
            if name in aliases[list(aliases.keys())[i]]:
                print("refactored")
                elem["user"] = list(aliases.keys())[i]

    os.remove(chat_path)

    with open(chat_path, "x") as f:
        json.dump({"messages": d}, f)

def getHours():
    with open(chat_path) as f:
        d = json.load(f)["messages"]

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

def addLists(x, y):
    if not len(x) == len(y):
        print("Addlists Error, terminating...")
        quit()
    else:
        c = []
        for i in range(len(x)):
            c.append(int(x[i]) + int(y[i]))

        return c