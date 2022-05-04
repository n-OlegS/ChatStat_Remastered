import json

d = {"messages" : []}
with open("./res/chat.json", 'w') as f:
    json.dump(d, f)