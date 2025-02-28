import json
def importJSON(stuff):
    with open(stuff,'r') as file:
        data = json.load(file)
        return(data)
def raceHistoryCount():
    history = importJSON('raceHistory.json')
    count = 0
    for i in history:
        count = count+1
    return count
print(raceHistoryCount())


    