import json, os, random

try:
    import clr
    clr.AddReference("IronPython.Modules.dll")
except:
    pass

import re

reference = re.compile(r"\[\[((?:[^\]]|(?:\](?!\])))*)\]\]")

def resolve_recursive(data, key):
    values = []
    for entry in data[key]:
        match = reference.match(entry)
        if match:
            values += resolve_recursive(data, match.group(1))
        else:
            values += [entry]
    return values

with open(os.path.join(os.path.dirname(__file__), "data.json"), mode='r') as file:
    config = json.load(file)

data = {}
for key in config['data']:
    data[key] = resolve_recursive(config['data'], key)

messages = config['messages']

def generate(protagonist = None):
    story = random.choice(messages)
    chosen = []
    for key in reference.findall(story):
        if key == "protagonist" and protagonist:
            choice = protagonist
        else:
            choice = random.choice(data[key])
            while choice in chosen:
                choice = random.choice(data[key])
            chosen += [choice]
        story = story.replace("[[" + key + "]]", choice, 1)
    return story

if __name__ == "__main__":
    print(generate())
