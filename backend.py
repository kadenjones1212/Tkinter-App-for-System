import time
import datetime
from datetime import datetime
import systemVariables as sys
import random as rand
import json
# Global variables to keep track of the timer state
global elapsedTime, startTime, timerRunning
elapsedTime = 0
startTime = 0
finishTime = 0
timerRunning = False
pauseTimeOffset = 0
timerTurnedOn = False

#General Stuff

def writeToFile(file,content,close = False):
    fileToEdit = open(file,'a')
    fileToEdit.write(content)
    if close == True:
        fileToEdit.close()
        
def settingsRewrite(line,object):#Function to change settings
    with open('systemVariables.py', 'r') as file: 
        data = file.readlines()
        data[line] = object
    with open('systemVariables.py', 'w') as file: 
        file.writelines(data) 
        
def importJSON(stuff):
    with open(stuff,'r') as file:
        data = json.load(file)
        return(data)
    
def clearFile(file):
    open(file, "w").close()

clearFile('activeRace.json')

#Settings Stuff#######################################
   
    
#Timer Management############################################

def startTimer():
    global startTime, finishTime, timerRunning, elapsedTime, pauseTimeOffset,timerTurnedOn
    elapsedTime = 0
    timerRunning = True
    
    newRaceData = {
        "runType" : sys.runType,
        "runDistance": sys.runDistance,
        "date" : getToday(),
        "events":[]
    }
    writeToFile('activeRace.json',json.dumps(newRaceData,indent = 2))
    
    #NEED TO CHANGE TO JSON
   
    startTime = time.perf_counter()

def pullTimer():
    global startTime, finishTime, timerRunning, elapsedTime, pauseTimeOffset
    elapsedTime = time.perf_counter() - startTime - pauseTimeOffset
    return elapsedTime

def stopButtonPressed(func):
    global startTime, finishTime, timerRunning, elapsedTime, pauseTimeOffset, timerTurnedOn
    
    #NEED TO CHANGE TO JSON
    timerRunning = False
    finishTime = pullTimer()
    return func


    

#Active Race Management#######################################################
def rawTimeConvert(): 
        rawTime = pullTimer()
        milliseconds = int((rawTime % 1) * 1000)
        seconds = int(rawTime) % 60
        minutes = (int(rawTime) // 60) % 60
        hours = int(rawTime) // 3600
        convertedTime = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
        return convertedTime

def rawTimeConvertOther(rawTime): #Same function but converts any input
        
        milliseconds = int((rawTime % 1) * 1000)
        seconds = int(rawTime) % 60
        minutes = (int(rawTime) // 60) % 60
        hours = int(rawTime) // 3600
        convertedTime = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
        return convertedTime

def getToday():
     revisedDate = datetime.now().strftime("%c")
     return revisedDate
def getShortToday():
    revisedDate = datetime.now().strftime("%d/%m/%y\n%I:%M %p")
    return revisedDate

            
    
        

    
    
def runnerRecord(id,format):#Mark Lap or Finish time of a runner
    lapEvent = {
        "eventType": "runnerLap" if format == 'runnerLap' else "runnerEnd",
        "runnerID": id,
        "raceTime": rawTimeConvert(),
    }
    with open('activeRace.json', 'r') as file:
        activeRaceFile = json.load(file)
    activeRaceFile["events"].append(lapEvent)
    with open('activeRace.json', 'w') as file:
        json.dump(activeRaceFile, file, indent=2)
#Close the file after race is over

def lap():#System Lap
    # lapEvent = {"eventType":"systemLap","raceTime":rawTimeConvert(),"date":getToday()}
    # with open('activeRace.json','r') as file:
    #     activeRaceFile = json.load(file)
    # activeRaceFile["events"].append(lapEvent)
    # with open('activeRace.json','w') as file:
    #     json.dump(activeRaceFile, file, indent = 2)
    runnerRecord(rand.choice([1111,2222,3333,4444,5555,6666,7777,8888]),"runnerLap")#Only for debugging purposes
    
def saveButtonPressed(func):
    try:
        activeRace = json.load(open("activeRace.json"))
        raceHistory = json.load(open("raceHistory.json"))
        raceHistory.append(activeRace)
        json.dump(raceHistory, open("raceHistory.json", "w"), indent=2)
        clearTempLog()
        print("Save successful")
    except Exception as e:
        print(f"Error saving race data: {e}")
    return func


def clearTempLog():
    raceLog = open("activeRace.json", "w").close()#clear the active race for use next time


    


    
 


         
