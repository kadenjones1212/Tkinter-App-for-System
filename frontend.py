#Last Updated 2/27/2025 10:21
import tkinter as tk
import systemVariables as sys
import backend as back
import time
from tkinter import PhotoImage
import math

# Initialize the main window
root = tk.Tk()
root.attributes('-fullscreen',True)
back.settingsRewrite(0,f'scn_w = {root.winfo_screenwidth()}\n')
back.settingsRewrite(1,f'scn_h = {root.winfo_screenheight()}\n')
historyPage = 0#For viewing history
raceResultPage = 0
root.geometry(str(sys.scn_w) + 'x' + str(sys.scn_h))
root.configure(bg=sys.cSecond)
root.config(cursor=None)
back.clearTempLog() #Clear the activeRace.json on bootup to make sure no errors arise when logging a race
#root.resizable(False,False)
def clearScreen():# Function to clear the screen by destroying all widgets
    for widget in root.winfo_children():
        widget.destroy()


        
# Header Setup
def updateHeader(vtext,boolIcons = True):
    global topHeader
    global topHeader_h
    topHeader = tk.Label(root, bg=sys.cMain)
    topHeader_h = sys.scn_h / 8
    topHeader.place(x=0, y=0, width=sys.scn_w, height=topHeader_h)
    headerTitle = tk.Label(topHeader, text=root.title(), bg=sys.cMain, fg=sys.cWhite, font=('Lexend', int(sys.scn_h / 25), 'bold'), anchor='w')
    headerTitle.place(x=10, y=0, width=sys.scn_w, height=topHeader_h)
    headerTitle.config(text=root.title())
    root.title(vtext)
    headerTitle.config(text=root.title())

    global settingsIconButton
    global homeIconButton
    global closeIconButton
    icon_size = int(sys.scn_h / 10)  # Same size as the current main title
    if boolIcons == True:
        settingsIconButton = makeDefaultButton('⚙️', settingsScreen,int(sys.scn_h / 25),'#666666','#333333')
        settingsIconButton.place(x=sys.scn_w - 2*icon_size, y=0, width=icon_size, height=icon_size)  # Adjust position and size as needed

        homeIconButton = makeDefaultButton('⌂', mainMenuScreen,int(sys.scn_h / 25),'#007777','#004444')
        homeIconButton.place(x=sys.scn_w - 3*icon_size, y=0, width=icon_size, height=icon_size)  # Adjust position and size as needed
        
        closeIconButton = makeDefaultButton('✖', closeApp,int(sys.scn_h / 25),'#ff0000','#aa0000')
        closeIconButton.place(x=sys.scn_w - icon_size, y=0, width=icon_size, height=icon_size)
        
        backIconButton = makeDefaultButton('<',None,int(sys.scn_h / 25),'#000000','#444444')
        backIconButton.place(x=sys.scn_w - 5*icon_size, y=0, width=icon_size*2, height=icon_size)
        
        

# Footer Setup
def updateFooter():
    global logoImageLabel
    global logoImage
    logoImage = PhotoImage(file=r'images/PTC_Logo.png')
    resized_logoImage = logoImage.subsample(int(8 / (sys.scn_h / 400)))  # resizing image
    logoImageLabel = tk.Label(root, image=resized_logoImage, bg=sys.cMain, anchor='w')
    logoImageLabel.image = resized_logoImage  # Keep a reference to the image
    logoImageLabel.pack(side=tk.LEFT, anchor='w')
    logoImageLabel.place(x=0, y=sys.scn_h - sys.scn_h / 8, width=sys.scn_w, height=sys.scn_h / 8)  # Adjust height as needed

# Function to create default buttons
def makeDefaultButton(vtext, vcommand, vsize=int(sys.scn_h / 25),color = sys.cMain,clickColor = sys.cSecond):
    return tk.Button(root,
                     text=vtext,
                     font=('Lexend',vsize ,'bold'),
                     background=color,
                     foreground=sys.cWhite,
                     activebackground=clickColor,
                     activeforeground=sys.cWhite,
                     borderwidth=sys.scn_h / 150,
                     command=vcommand)
def makeDefaultLabel(vtext, vsize=int(sys.scn_h/25),anchor=None,color=sys.cMain):
    return tk.Label(root,
                    text=vtext,
                    font=('Lexend', vsize,'bold'),
                    background=color,
                    foreground=sys.cWhite,
                    borderwidth=0,
                    anchor = anchor
                    )

def clockLabel(vtext,vcommand,fontSize = int(sys.scn_w / 10)):
    return tk.Label(root,
                     text = vtext,
                     font=('Consolas', fontSize,'bold'),
                     background=sys.cMain,
                     foreground=sys.cWhite,
                     activeforeground=sys.cWhite,
                     #borderwidth=sys.scn_h / 75,
                     )

def makeColorButton(vtext,vcommand,vcolor):
    return tk.Button(root,
                     text=vtext,
                     font=('Lexend', int(sys.scn_h / 25),'bold'),
                     background = vcolor,
                     foreground=sys.cWhite,
                     activebackground = vcolor,
                     activeforeground=sys.cWhite,
                     borderwidth=sys.scn_h / 150,
                     command=vcommand)
    
def confirmChoice(prompt,funcYes, funcNo):
    promptLabel = makeDefaultLabel(prompt,int(sys.scn_h/8))
    promptLabel.place(x=0, y=0, width=sys.scn_w, height=sys.scn_h*0.75)
    yesButton = makeColorButton('Yes',lambda: funcYes(),'#ff0000')
    yesButton.place(x=0, y=sys.center_y*1.5, width=sys.scn_w/4, height=sys.scn_h/4)
    noButton = makeColorButton('No',lambda: destroyYesNoScreen(),'#00aa00')
    noButton.place(x=sys.center_x*0.5, y=sys.center_y*1.5, width=sys.scn_w*.75, height=sys.scn_h/4)
    def destroyYesNoScreen():
        yesButton.destroy()
        promptLabel.destroy()
        noButton.destroy()
    
# Main Menu Screen####################################################################################################
def mainMenuScreen():
    clearScreen()
    updateHeader('Main Menu')
    updateFooter()

    # Start race button
    startRaceButton = makeDefaultButton('Start A Race', raceSelectScreen)
    startRaceButton.place(x=sys.scn_w/16,
                          y=sys.scn_h/4,
                          width=sys.scn_w/2-sys.scn_w/8,
                          height=sys.scn_h/2)

    # History button
    historyButton = makeDefaultButton('Race History', raceHistoryScreen)
    historyButton.place(x=sys.scn_w/16+ sys.scn_w/2,
                          y=sys.scn_h/4,
                          width=sys.scn_w/2-sys.scn_w/8,
                          height=sys.scn_h/2)
    
    cornerClockDisplay()
    
#Settings Screen####################################################################################

def settingsScreen():
    clearScreen()
    updateHeader('Settings')
    updateFooter()
    
    settingsButton = makeDefaultButton('Units',None)
    settingsButton.place(x=0, y=sys.center_y - 3 * sys.mainButton_h, width=sys.scn_w, height=sys.mainButton_h)
    settingsButton = makeDefaultButton('Date/Time',None)
    settingsButton.place(x=0, y=sys.center_y - 2 * sys.mainButton_h, width=sys.scn_w, height=sys.mainButton_h)
    settingsButton = makeDefaultButton('Export Data',None)
    settingsButton.place(x=0, y=sys.center_y - 1 * sys.mainButton_h, width=sys.scn_w, height=sys.mainButton_h)
    settingsButton = makeDefaultButton('Import Data',None)
    settingsButton.place(x=0, y=sys.center_y - 0 * sys.mainButton_h, width=sys.scn_w, height=sys.mainButton_h)
    settingsButton = makeDefaultButton('Erase History',lambda: confirmChoice('Erase History?',lambda: eraseHistory(),lambda: settingsScreen()))
    settingsButton.place(x=0, y=sys.center_y + 1 * sys.mainButton_h, width=sys.scn_w, height=sys.mainButton_h)

    saveSettingsButton = makeDefaultButton('Save Settings', None)
    saveSettingsButton.place(x = 0, y = sys.scn_h - sys.scn_h/8-sys.mainButton_h, width=sys.scn_w, height=sys.mainButton_h)
    cornerClockDisplay()
#Erase History#########################################################################################################
def eraseHistory():
    back.clearFile('raceHistory.json')
    back.writeToFile('raceHistory.json','[]')
    mainMenuScreen()
# Race Select Screen####################################################################################################

def raceSelectScreen():
    clearScreen()
    updateHeader('Race Select')
    updateFooter()

    # Start race button
    dist5KButton = makeDefaultButton('5K', lambda: rScn('5K'))
    dist5KButton.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y - 2 * sys.mainButton_h, width=sys.mainButton_w, height=sys.mainButton_h)

    # History button
    dist10KButton = makeDefaultButton('10K', lambda: rScn('10K'))
    dist10KButton.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y - 2 * sys.mainButton_h / 2, width=sys.mainButton_w, height=sys.mainButton_h)

    # Calibrate button
    distTrackButton = makeDefaultButton('Track', trackSetup)
    distTrackButton.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y + 0 * sys.mainButton_h / 2, width=sys.mainButton_w, height=sys.mainButton_h)

    # Setup help button (NOT THE SAME AS SETTINGS)
    distCustomButton = makeDefaultButton('Custom', None)
    distCustomButton.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y + 1 * sys.mainButton_h, width=sys.mainButton_w, height=sys.mainButton_h)
    cornerClockDisplay()
# Start Races Screens####################################################################################################

def rScn(raceDist):
    clearScreen()
    sys.runDistance = raceDist
    updateHeader(sys.runDistance + ' Race')
    updateFooter()
    startButton = makeDefaultButton(f'{sys.runDistance} Start', startTimer)
    startButton.place(x=sys.center_x - sys.mainButton_w * 1.25 / 2, y=sys.center_y - sys.mainButton_h*2, width=sys.mainButton_w * 1.25, height=sys.mainButton_h * 4)
    cornerClockDisplay()

def trackSetup(): 
    clearScreen()
    updateHeader('Track Setup')
    updateFooter()

    dist400Button = makeDefaultButton('400m', lambda: rScn('400m'))
    dist400Button.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y - 2 * sys.mainButton_h, width=sys.mainButton_w, height=sys.mainButton_h)

    dist800Button = makeDefaultButton('800m', lambda: rScn('800m'))
    dist800Button.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y - 2 * sys.mainButton_h / 2, width=sys.mainButton_w, height=sys.mainButton_h)

    dist1600Button = makeDefaultButton('1600m', lambda: rScn('1600m'))
    dist1600Button.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y + 0 * sys.mainButton_h / 2, width=sys.mainButton_w, height=sys.mainButton_h)

    dist3200Button = makeDefaultButton('3200m', lambda: rScn('3200m'))
    dist3200Button.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y + 1 * sys.mainButton_h, width=sys.mainButton_w, height=sys.mainButton_h)
#Race History Screen Main Menu###################################################################################################3
def raceHistoryScreen(historyPage=0):
    clearScreen()
    updateHeader(f'Race History ({back.raceHistoryCount()} Races)')
    updateFooter()
    cornerClockDisplay()
    
    upButton = makeDefaultButton('⇧',historyPageUp,int(sys.scn_h/20),'#007777','#007777')
    upButton.place(x=sys.scn_w- sys.scn_w/16, y=sys.scn_h/8, width=sys.scn_w/16, height=sys.scn_h/4*1.5)
    downButton = makeDefaultButton('⇩',historyPageDown,int(sys.scn_h/20),'#007777','#007777')
    downButton.place(x=sys.scn_w- sys.scn_w/16, y=sys.scn_h/2, width=sys.scn_w/16, height=sys.scn_h/4*1.5)
    
    for i in range(6):  # Construct List of Recent Races
        
        raceIndex = historyPage * 6 + i
        raceTitle = f"{back.getObjectFromJSON('raceHistory.json', raceIndex, 'runDistance')} - {back.getObjectFromJSON('raceHistory.json', raceIndex, 'date')}"
        if raceIndex < back.raceHistoryCount():
            indexLabel = makeDefaultLabel(raceIndex + 1, int(sys.scn_h / 16))
            indexLabel.place(x=0, y=sys.scn_h / 8 + sys.scn_h / 8 * i, width=sys.scn_w / 16, height=sys.mainButton_h)
        recentRaceButton = makeDefaultButton(raceTitle, lambda raceIndex=raceIndex: raceViewEndTimesScreen(raceIndex), int(sys.scn_h / 25))
        recentRaceButton.place(x=sys.scn_w / 16, y=sys.scn_h / 8 + sys.scn_h / 8 * i, width=sys.scn_w - sys.scn_w / 8, height=sys.mainButton_h)

def historyPageUp():
    global historyPage
    if historyPage == 0:
        None
    else:
        historyPage = historyPage-1
        raceHistoryScreen(historyPage)
        
def historyPageDown():
    global historyPage
    if (historyPage + 1) * 6 < back.raceHistoryCount():
        historyPage += 1
        raceHistoryScreen(historyPage)
        
#Viewing Individual Race Screen###########################################################
def raceResultPageUp(raceIndex):
    global raceResultPage
    if raceResultPage == 0:
        None
    else:
        raceResultPage = raceResultPage - 1
        raceViewEndTimesScreen(raceIndex)

def raceResultPageDown(raceIndex):
    global raceResultPage
    if (raceResultPage + 1) * 6 < back.getNumberOfRunners(raceIndex):
        raceResultPage = raceResultPage + 1
        raceViewEndTimesScreen(raceIndex)
    
#View Race End times##############################################################################
def raceViewEndTimesScreen(raceIndex):
    clearScreen()
    updateHeader(f'Results:  {back.getRaceTitle(raceIndex)}')
    updateFooter()
    cornerClockDisplay()
    
    upButton = makeDefaultButton('⇧', lambda: raceResultPageUp(raceIndex), int(sys.scn_h / 20), '#007777', '#007777')
    upButton.place(x=sys.scn_w - sys.scn_w / 16, y=sys.scn_h / 8, width=sys.scn_w / 16, height=sys.scn_h / 4 * 1.5)
    downButton = makeDefaultButton('⇩', lambda: raceResultPageDown(raceIndex), int(sys.scn_h / 20), '#007777', '#007777')
    downButton.place(x=sys.scn_w - sys.scn_w / 16, y=sys.scn_h / 2, width=sys.scn_w / 16, height=sys.scn_h / 4 * 1.5)

    spacing = sys.scn_h/16+sys.scn_h/64
    resultsPerScreen = 8
    rowHeight = sys.scn_h/16
    bgLine = makeDefaultLabel(None,1,None,sys.cMain)
    bgLine.place(x=0, y=sys.scn_h / 8 , width=sys.scn_w-sys.scn_w/16, height=sys.scn_h/16)

    indexTitleLabel = makeDefaultLabel('#', int(sys.scn_h / 32))
    indexTitleLabel.place(x=0, y=sys.scn_h / 8 + sys.scn_h/16 + spacing * -1, width=sys.scn_w / 16, height=rowHeight)
    runnerIDLabel = makeDefaultLabel('Runner',int(sys.scn_h / 32))
    runnerIDLabel.place(x=sys.scn_w / 8, y=sys.scn_h / 8  + sys.scn_h/16+ spacing *-1, width=sys.scn_w / 8, height=rowHeight)
    raceTimeLabel = makeDefaultLabel('Time',int(sys.scn_h / 32))
    raceTimeLabel.place(x=sys.scn_w / 4 +sys.scn_w/16, y=sys.scn_h / 8 + sys.scn_h/16+ spacing * -1, width=sys.scn_w / 4, height=rowHeight)
    horizLine = makeDefaultLabel(None,1,None,'Black')
    horizLine.place(x=0, y=sys.scn_h / 8+sys.scn_h/32+sys.scn_h/64 , width=sys.scn_w-sys.scn_w/16, height=sys.scn_h/32)
    
    raceEvents = back.getObjectFromJSON('raceHistory.json',raceIndex,'events')
    raceFinishEvents = [event for event in raceEvents if event['eventType'] == 'runnerEnd']
    for i in range(resultsPerScreen):
        runnerIndex = raceResultPage * resultsPerScreen + i
        if runnerIndex < back.getNumberOfRunners(raceIndex):
            
            placementID = f"{raceFinishEvents[runnerIndex]['runnerID']}"
            placementTime = f"{raceFinishEvents[runnerIndex]['raceTime']}"
            
            indexLabel = makeDefaultLabel(runnerIndex + 1, int(sys.scn_h / 18))
            indexLabel.place(x=0, y=sys.scn_h / 8 + sys.scn_h/16 +sys.scn_h/32 + spacing * i, width=sys.scn_w / 16, height=rowHeight)
           
            recentRaceID = makeDefaultLabel(placementID, int(sys.scn_h / 25))
            recentRaceID.place(x=sys.scn_w / 8, y=sys.scn_h / 8 +sys.scn_h/32 + sys.scn_h/16+ spacing * i, width=sys.scn_w / 8, height=rowHeight)
            
            placementTimeLabel = makeDefaultLabel(placementTime, int(sys.scn_h / 25))
            placementTimeLabel.place(x=sys.scn_w / 4 +sys.scn_w/16, y=sys.scn_h / 8  +sys.scn_h/32+ sys.scn_h/16+ spacing * i, width=sys.scn_w / 4, height=rowHeight)
            
            detailedRunnerStatButton = makeDefaultButton("Stats", lambda runner=runnerIndex: viewDetailedRunnerStats(raceIndex, raceFinishEvents[runner]["runnerID"]), int(sys.scn_h / 25), 'Black')
            detailedRunnerStatButton.place(x=sys.scn_w -sys.scn_w/16-sys.scn_w/8, y=sys.scn_h / 8  +sys.scn_h/32+ sys.scn_h/16+ spacing * i, width=sys.scn_w / 8, height=rowHeight)
            
    def viewDetailedRunnerStats(raceIndex,runner):
        clearScreen()
        updateHeader(f'Runner {runner} | {back.getRaceDistance(raceIndex)}')
        updateFooter()
        cornerClockDisplay()
        placement = 1
        for event in raceFinishEvents:
            if event['runnerID'] == runner:
                break
            placement += 1
        finishTimeLabel= makeDefaultLabel(
            f'Runner ID: {runner}\nFinish Time: {back.getRunnerFinishTime(raceIndex,runner)}\nPlace: {placement}',
            int(sys.scn_h/24),"nw",sys.cSecond)
        finishTimeLabel.place(x=0,y=sys.scn_h/8,width=sys.scn_w,height=sys.scn_h/2)
    
#Cross Country Race ####################################################################################################

def startTimer():
    clearScreen()
    updateHeader('Timer Start',False)
    updateFooter()
    startTimerButton = makeColorButton(f'BEGIN {sys.runDistance} RACE',lambda: timerScreen(), 'Green')
    startTimerButton.place(x=0, y=sys.scn_h/8, width=sys.scn_w, height=sys.scn_h*0.75-sys.scn_h/8)
    cancelButton = makeDefaultButton('Cancel',mainMenuScreen)
    cancelButton.place(x = 0, y = sys.scn_h - sys.scn_h/8-sys.scn_h/8, width=sys.scn_w, height=sys.scn_h/8)
    cornerClockDisplay()
#Timer Screen Management####################################################################################################
def updateClock():
    if back.timerRunning == True:
        displayClock.config(text = back.rawTimeConvert())
        root.after(1, updateClock)
    else:
        displayClock.config(text = back.rawTimeConvertOther(back.finishTime))
        # root.after(1, updateClock)

def timerButtons(vOn):
    
    if vOn == True:
        lapButton = makeDefaultButton('Lap', lambda: back.lap())
        lapButton.place(x=0, y=sys.scn_h-sys.scn_h/8-sys.mainButton_h*1.5, width=sys.scn_w/(3/2), height=sys.mainButton_h * 1.5)
        stopButton = makeColorButton('Stop', lambda: confirmChoice('End Race?',lambda: back.stopButtonPressed(timerScreen(False)),None), 'Red')
        stopButton.place(x=sys.scn_w*(2/3),y=sys.scn_h-sys.scn_h/8-sys.mainButton_h*1.5, width=sys.scn_w/3, height=sys.mainButton_h * 1.5)
    elif vOn == False:
        
        saveButton = makeDefaultButton('Save',lambda: back.saveButtonPressed(mainMenuScreen()))
        saveButton.place(x=0, y=sys.scn_h-sys.scn_h/8-sys.mainButton_h*1.5, width=sys.scn_w, height=sys.mainButton_h * 1.5)
        #resumeButton = makeColorButton('Resume',lambda: back.resumeTimer(timerScreen(True)),'Green')
        #resumeButton.place(x=sys.center_x,y=sys.scn_h-sys.scn_h/8-sys.mainButton_h*1.5, width=sys.scn_w/2, height=sys.mainButton_h * 1.5)

def timerScreen(vTimerOn = True):
    global displayClock
    clearScreen()
    if vTimerOn == True:
        back.startTimer()
    updateHeader(sys.runDistance + ' In Progress', False)
    updateFooter()
    cornerClockDisplay()
    displayClock = clockLabel(back.elapsedTime, None)
    displayClock.place(
        x = 0,
        y = sys.scn_h /8,
        width = sys.scn_w,
        height = sys.scn_h/2
        )
    if vTimerOn == True:
        timerButtons(True)
    else:
        timerButtons(False)
    updateClock()
    
#OnScreen Time of day clock###########################################################################

def cornerClockDisplay():
    cornerClock = clockLabel(back.getShortToday(), None, int(sys.scn_h / 32))
    cornerClock.place(
        x = sys.scn_w/2,
        y = sys.scn_h/8,
        width = sys.scn_w,
        height = sys.scn_h/4
        )
    def updateCornerClock():
        cornerClock.config(text=back.getShortToday())
        root.after(1000, updateCornerClock)  # Update every second
        
    
    
    cornerClock.place(
        x=sys.scn_w-sys.scn_w/8,
        y=sys.scn_h-sys.scn_h/8,
        width=sys.scn_w / 8,
        height=sys.scn_h / 8
    )
    
    updateCornerClock() 

#Kill Program################################################################################################
def closeApp():
    confirmChoice('Exit\nPortaTrack\nConnect?',lambda: root.destroy(),lambda: mainMenuScreen())
   

####################################################################################################
# Start by showing the main menu screen
####################################################################################################
####################################################################################################
####################################################################################################
mainMenuScreen()
root.mainloop()
