#Last Updated 2/27/2025 10:21
import tkinter as tk
import systemVariables as sys
import backend as back
import time
from tkinter import PhotoImage

# Initialize the main window
root = tk.Tk()
root.attributes('-fullscreen',True)
back.settingsRewrite(0,f'scn_w = {root.winfo_screenwidth()}\n')
back.settingsRewrite(1,f'scn_h = {root.winfo_screenheight()}\n')


root.geometry(str(sys.scn_w) + 'x' + str(sys.scn_h))

root.configure(bg=sys.cSecond)
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
    global settingsIcon
    global homeIconButton
    global homeIcon
    global closeIconButton
    global closeIcon

    settingsIcon = '⚙️'
    homeIcon = '⌂'
    closeIcon = '✖'
    icon_size = int(sys.scn_h / 10)  # Same size as the current main title
    if boolIcons == True:
        settingsIconButton = makeDefaultButton(settingsIcon, settingsScreen)
        settingsIconButton.place(x=sys.scn_w - 2*icon_size - int(sys.scn_h / 80), y=(topHeader_h - icon_size) / 2, width=icon_size, height=icon_size)  # Adjust position and size as needed

        homeIconButton = makeDefaultButton(homeIcon, mainMenuScreen)
        homeIconButton.place(x=sys.scn_w - 3*icon_size - int(sys.scn_h / 80), y=(topHeader_h - icon_size) / 2, width=icon_size, height=icon_size)  # Adjust position and size as needed
        
        closeIconButton = makeDefaultButton(closeIcon, closeApp)
        closeIconButton.place(x=sys.scn_w - icon_size - int(sys.scn_h / 80), y=(topHeader_h - icon_size) / 2, width=icon_size, height=icon_size)
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
def makeDefaultButton(vtext, vcommand, vsize=int(sys.scn_h / 25),color = sys.cMain):
    return tk.Button(root,
                     text=vtext,
                     font=('Lexend',vsize ,'bold'),
                     background=color,
                     foreground=sys.cWhite,
                     activebackground=sys.cSecond,
                     activeforeground=sys.cWhite,
                     borderwidth=sys.scn_h / 150,
                     command=vcommand)
def makeDefaultLabel(vtext, vsize=int(sys.scn_h/25),):
    return tk.Label(root,
                    text=vtext,
                    font=('Lexend', vsize,'bold'),
                    background=sys.cMain,
                    foreground=sys.cWhite,
                    borderwidth=0,
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
    startRaceButton.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y - 2 * sys.mainButton_h, width=sys.mainButton_w, height=sys.mainButton_h)

    # History button
    historyButton = makeDefaultButton('Race History', raceHistoryScreen)
    historyButton.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y - 2 * sys.mainButton_h / 2, width=sys.mainButton_w, height=sys.mainButton_h)

    # Calibrate button
    calibrateButton = makeDefaultButton('Calibrate', None)
    calibrateButton.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y + 0 * sys.mainButton_h / 2, width=sys.mainButton_w, height=sys.mainButton_h)

    # Setup help button (NOT THE SAME AS SETTINGS)
    setupHelpButton = makeDefaultButton('Setup Help', None)
    setupHelpButton.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y + 1 * sys.mainButton_h, width=sys.mainButton_w, height=sys.mainButton_h)
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
    startButton.place(x=sys.center_x - sys.mainButton_w * 1.25 / 2, y=sys.center_y - sys.mainButton_h, width=sys.mainButton_w * 1.25, height=sys.mainButton_h * 2)
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
def raceHistoryScreen(page=0):
    clearScreen()
    updateHeader(f'Race History ({back.raceHistoryCount()} Races)')
    updateFooter()
    cornerClockDisplay()
    upButton = makeDefaultButton('⇧',None,int(sys.scn_h/20),'#00aaaa')
    upButton.place(x=sys.scn_w- sys.scn_w/16, y=sys.scn_h/8, width=sys.scn_w/16, height=sys.scn_h/4*1.5)
    downButton = makeDefaultButton('⇩',None,int(sys.scn_h/20),'#00aaaa')
    downButton.place(x=sys.scn_w- sys.scn_w/16, y=sys.scn_h/2, width=sys.scn_w/16, height=sys.scn_h/4*1.5)
    if back.raceHistoryCount() < 6:
        overflowMax = back.raceHistoryCount()#testing
    else:
        overflowMax = 6
    for i in range(0,overflowMax):#Construct List of Recent Races
        indexLabel = makeDefaultLabel(i+1,int(sys.scn_h/16))
        indexLabel.place(x=0, y=sys.scn_h/8+sys.scn_h/8*i, width=sys.scn_w/16, height=sys.mainButton_h)
        recentRaceButton = makeDefaultButton(f"{back.getObjectFromJSON('raceHistory.json', i, 'runDistance')} - {back.getObjectFromJSON('raceHistory.json', i, 'date')}", None, int(sys.scn_h / 25))

        recentRaceButton.place(x=sys.scn_w/16, y=sys.scn_h/8+sys.scn_h/8*i, width=sys.scn_w-sys.scn_w/8, height=sys.mainButton_h)
    
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
        height = sys.scn_h/4
        )
    if vTimerOn == True:
        timerButtons(True)
    else:
        timerButtons(False)
    updateClock()
    
#OnScreen Time of day clock###############################

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

#Kill Program
def closeApp():
    confirmChoice('Exit\nPortaTrack\nConnect?',lambda: root.destroy(),lambda: mainMenuScreen())
   

####################################################################################################
# Start by showing the main menu screen
####################################################################################################
####################################################################################################
####################################################################################################
mainMenuScreen()
root.mainloop()
