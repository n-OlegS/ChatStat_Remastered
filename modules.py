import datetime


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