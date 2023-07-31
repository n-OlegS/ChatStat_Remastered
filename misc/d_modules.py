import datetime, json, os, time

with open(os.getcwd()[:os.getcwd().find("chatstat") + 19] + '/misc/config.json') as f:
    chat_path = json.load(f)["chat.json path"]

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
