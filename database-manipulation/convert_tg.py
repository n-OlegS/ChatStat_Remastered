import json
from misc.d_modules import generate_tg

with open("./res/chat.json", 'w') as f:
    json.dump(generate_tg(input()), f)

