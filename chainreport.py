import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

TOKEN = os.getenv("TORN_KEY")

timefrom = int(input("When from? "))
timeto = int(input("When to? "))

# get chain info!
print("Getting chain info...")
chains = requests.get(f"https://api.torn.com/faction/?selections=chains&key={TOKEN}&from={timefrom}&to={timeto}")
chains = json.loads(chains.content)["chains"]
print(f"Loaded {len(chains)} chains")

contribs = {}

for chainid in chains:
    print(f"Processing chain {chainid}")
    info = requests.get(f"https://api.torn.com/torn/{chainid}/?selections=chainreport&key={TOKEN}")
    info = json.loads(info.content)["chainreport"]
    members = info["members"]

    for m, mdata in members.items():
        if mdata["attacks"] >= 4: # if enough hits
            if m not in contribs.keys():
                contribs[m] = mdata["attacks"] # if not in dict, add member
            else: contribs[m] += mdata["attacks"] # add number of hits

print(contribs)