import time
import datetime
from datetime import datetime
import systemVariables as sys
import random as rand
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

#Settings Stuff#######################################
   
    
#Timer Management############################################

def startTimer():
    global startTime, finishTime, timerRunning, elapsedTime, pauseTimeOffset,timerTurnedOn
    elapsedTime = 0
    timerRunning = True
    systemStartTime = f'{sys.raceDistance} RESUME | Date, {getToday()}\n'
    #NEED TO CHANGE TO JSON
    activeRaceFile = open("activeRace.json", "a")
    activeRaceFile.write(systemStartTime)
    startTime = time.perf_counter()

def pullTimer():
    global startTime, finishTime, timerRunning, elapsedTime, pauseTimeOffset
    elapsedTime = time.perf_counter() - startTime - pauseTimeOffset
    return elapsedTime

def stopButtonPressed(func):
    global startTime, finishTime, timerRunning, elapsedTime, pauseTimeOffset, timerTurnedOn
    #writeToFile('activeRace.json',f'{sys.raceDistance} PAUSED | RaceTime, {rawTimeConvert()} | Date, {getToday()}\n')
    #NEED TO CHANGE TO JSON
    timerRunning = False
    finishTime = pullTimer()
    return func

def resumeTimer(func):
    global startTime, finishTime, timerRunning, elapsedTime, pauseTimeOffset
    pauseTimeOffset = time.perf_counter()- (startTime + finishTime)
    return func
    

#Active Race Management#######################################################
def rawTimeConvert(): 
#Used AI to make converter this since I didn't want to do the math. 
# Just simple stuff that I COULD have done, but was tedious, so I just was lazy 
# and had AI do the dirty work. This is the only section of code that wasn't written
# entirely by me.
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
    revisedDate = datetime.now().strftime("%d/%m/%y\n%H:%M")
    return revisedDate

            
    
        
def lap():#System Lap
    writeToFile('activeRace.json',f'SystemLap | LapTime, {rawTimeConvert()} | Date, {getToday()}\n')
    #NEED TO CHANGE TO JSON
    
def runnerRecord(id,format):#Mark Lap or Finish time of a runner
    if format == 'Lap':
        writeToFile('activeRace.json',f'RunnerLap: {id} | LapTime, {rawTimeConvert()} | Date, {getToday()}\n')
        #NEED TO CHANGE TO JSON
    elif format == 'Finish':
        writeToFile('activeRace.json',f'RunnerEnd: {id} | EndTime, {rawTimeConvert()} | Date, {getToday()}\n')
        #NEED TO CHANGE TO JSON
#Close the file after race is over

def saveButtonPressed(func):
    writeToFile('activeRace.json',
                f'{sys.raceDistance} END | EndTime, {rawTimeConvertOther(finishTime)} | Date, {getToday()}',
                True
                )
    #NEED TO CHANGE TO JSON
    constructRaceResults()
    return func

def getLineInfo(stuff):#Remove vertical line and turn into list
    thing = stuff.split('|')
    return thing

def clearTempLog():
    raceLog = open("activeRace.json", "w").close()#clear the active race for use next time
def constructRaceResults():
    raceLog = open("activeRace.json", "r")
    raceText = raceLog.read()
    raceLog.close()
    writeToFile('raceHistory.txt',f'{raceText}\n\n',True)
    #NEED TO CHANGE TO JSON
    clearTempLog()

    


    
 


         
