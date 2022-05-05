from misc.modules import generate_tg, generate_wa
import json, time, os
from datetime import datetime


tg = generate_tg(input("Telegram export path: "))["messages"]
wa = generate_wa(input("Whatsapp export path: "))["messages"]

with open(os.getcwd() + '/config.json') as f:
    chat_path = json.load(f)["chat.json path"]

out = []

while not (len(tg) == 0 and len(wa) == 0):
    if len(wa) == 0:
        tg_mess = tg[0]
        out.append(tg_mess)
        del tg[0]
        continue
    elif len(tg) == 0:
        wa_mess = wa[0]
        out.append(wa_mess)
        del wa[0]
        continue

    wa_mess = wa[0]
    tg_mess = tg[0]

    if datetime.fromtimestamp(time.mktime(wa_mess["time"])) < datetime.fromtimestamp(time.mktime(tg_mess["time"])):
        out.append(wa_mess)
        del wa[0]
    else:
        out.append(tg_mess)
        del tg[0]

os.remove(chat_path)

with open(chat_path, "x") as f:
    json.dump({"messages" : out}, f)