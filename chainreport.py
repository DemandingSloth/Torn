import os
from dotenv import load_dotenv
import requests
import json
import time

load_dotenv()

TOKEN = os.getenv("TORN_KEY")

# get time inputs
timefrom = int(input("When from? "))
timeto = input("When to? ")
if timeto == "now": timeto = int(time.time()) # if user says "now", get current time
else: timeto = int(timeto)

# get list of chains!
print("Getting chain info...")
chains = json.loads(requests.get(f"https://api.torn.com/faction/?selections=chains&key={TOKEN}&from={timefrom}&to={timeto}").content)
if "error" in chains: # look for potential error in response 
    print(f"\nError:\n{chains}")
    exit()
else: chains = chains["chains"]
print(f"Loaded {len(chains)} chains")
contribs = {}

for chainid in chains:
    print(f"Processing chain {chainid}")
    info = json.loads(requests.get(f"https://api.torn.com/torn/{chainid}/?selections=chainreport&key={TOKEN}").content)
    if "error" in info: # look for potential error in response 
        print(f"\nError:\n{chains}")
        exit()
    else: info = info["chainreport"]
    members = info["members"]

    for member_id, mdata in members.items():
        if mdata["attacks"] >= 3:  
            if member_id not in contribs.keys():
                contribs[member_id] = mdata["attacks"]
            else:
                contribs[member_id] += mdata["attacks"]

print("Getting usernames...\n")
time.sleep(1) # in case close to API limit

# Get member profiles and print results
print(f"Attacks\tName") 
for member_id, attacks in contribs.items():
    profileInfo = requests.get(f"https://api.torn.com/user/{member_id}/?key={TOKEN}")  # Removed selections=profile
    profileInfo = json.loads(profileInfo.content)
    name = profileInfo["name"] 
    print(f"{attacks}\t{name}") 

print(f"'to' time: {timeto}")