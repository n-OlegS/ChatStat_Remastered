import json
from misc.modules import generate_wa

with open("./res/chat.json", 'w') as f:
    json.dump(generate_wa(input()), f)
