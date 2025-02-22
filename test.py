import json

with open('raceHistory.json', 'r') as file:
    dict = json.load(file)
    
print(dict[0].get("events"))
# dump