import tkinter as tk
import systemVariables as sys
import backend as back
import time
from tkinter import PhotoImage

# Initialize the main window
root = tk.Tk()
root.geometry(str(sys.scn_w) + 'x' + str(sys.scn_h))
root.configure(bg=sys.cSecond)
back.clearTempLog() #Clear the activeRace.txt on bootup to make sure no errors arise when logging a race
root.resizable(False,False)
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

    settingsIcon = '⚙️'
    homeIcon = '🏠'
    icon_size = int(sys.scn_h / 10)  # Same size as the current main title
    if boolIcons == True:
        settingsIconButton = makeDefaultButton(settingsIcon, settingsScreen)
        settingsIconButton.place(x=sys.scn_w - icon_size - int(sys.scn_h / 80), y=(topHeader_h - icon_size) / 2, width=icon_size, height=icon_size)  # Adjust position and size as needed

        homeIconButton = makeDefaultButton(homeIcon, mainMenuScreen)
        homeIconButton.place(x=sys.scn_w - 2*icon_size - int(sys.scn_h / 80), y=(topHeader_h - icon_size) / 2, width=icon_size, height=icon_size)  # Adjust position and size as needed

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
def makeDefaultButton(vtext, vcommand):
    return tk.Button(root,
                     text=vtext,
                     font=('Lexend', int(sys.scn_h / 25),'bold'),
                     background=sys.cMain,
                     foreground=sys.cWhite,
                     activebackground=sys.cSecond,
                     activeforeground=sys.cWhite,
                     borderwidth=sys.scn_h / 75,
                     command=vcommand)

def clockLabel(vtext, vcommand,fontSize = int(sys.scn_w / 10)):
    return tk.Label(root,
                     text = vtext,
                     #thingything
                     font=('Consolas', fontSize,'bold'),
                     background=sys.cMain,
                     foreground=sys.cWhite,
                     #activebackground=sys.cSecond,
                     activeforeground=sys.cWhite,
                     #borderwidth=sys.scn_h / 75,
                     command=vcommand)

def makeColorButton(vtext,vcommand,vcolor):
    return tk.Button(root,
                     text=vtext,
                     font=('Lexend', int(sys.scn_h / 25),'bold'),
                     background = vcolor,
                     foreground=sys.cWhite,
                     activebackground = vcolor,
                     activeforeground=sys.cWhite,
                     borderwidth=sys.scn_h / 75,
                     command=vcommand)

# Main Menu Screen####################################################################################################
def mainMenuScreen():
    clearScreen()
    updateHeader('Main Menu')
    updateFooter()

    # Start race button
    startRaceButton = makeDefaultButton('Start A Race', raceSelectScreen)
    startRaceButton.place(x=sys.center_x - sys.mainButton_w / 2, y=sys.center_y - 2 * sys.mainButton_h, width=sys.mainButton_w, height=sys.mainButton_h)

    # History button
    historyButton = makeDefaultButton('Race History', None)
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
    settingsButton = makeDefaultButton('Erase History',None)
    settingsButton.place(x=0, y=sys.center_y + 1 * sys.mainButton_h, width=sys.scn_w, height=sys.mainButton_h)

    saveSettingsButton = makeDefaultButton('Save Settings', None)
    saveSettingsButton.place(x = 0, y = sys.scn_h - sys.scn_h/8-sys.mainButton_h, width=sys.scn_w, height=sys.mainButton_h)
    cornerClockDisplay()
    
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
    sys.raceDistance = raceDist
    updateHeader(sys.raceDistance + ' Race')
    updateFooter()
    startButton = makeDefaultButton(f'{sys.raceDistance} Start', startTimer)
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

    
#Cross Country Race ####################################################################################################

def startTimer():
    clearScreen()
    updateHeader('Timer Start',False)
    updateFooter()
    startTimerButton = makeColorButton(f'BEGIN {sys.raceDistance} RACE',lambda: timerScreen(), 'Green')
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
        stopButton = makeColorButton('Stop', lambda: back.stopButtonPressed(timerScreen(False)), 'Red')
        stopButton.place(x=sys.scn_w*(2/3),y=sys.scn_h-sys.scn_h/8-sys.mainButton_h*1.5, width=sys.scn_w/3, height=sys.mainButton_h * 1.5)
    elif vOn == False:
        
        saveButton = makeDefaultButton('Save',lambda: back.saveButtonPressed(mainMenuScreen()))
        saveButton.place(x=0, y=sys.scn_h-sys.scn_h/8-sys.mainButton_h*1.5, width=sys.scn_w/2, height=sys.mainButton_h * 1.5)
        resumeButton = makeColorButton('Resume',lambda: back.resumeTimer(timerScreen(True)),'Green')
        resumeButton.place(x=sys.center_x,y=sys.scn_h-sys.scn_h/8-sys.mainButton_h*1.5, width=sys.scn_w/2, height=sys.mainButton_h * 1.5)

def timerScreen(vTimerOn = True):
    global displayClock
    clearScreen()
    if vTimerOn == True:
        back.startTimer()
    updateHeader(sys.raceDistance + ' In Progress', False)
    updateFooter()
    cornerClockDisplay()
    displayClock = clockLabel(back.elapsedTime, None)
    displayClock.place(
        x = 0,
        y = sys.center_y - 2.5 * sys.mainButton_h,
        width = sys.scn_w,
        height = sys.mainButton_h*2
        )
    if vTimerOn == True:
        timerButtons(True)
    else:
        timerButtons(False)
    updateClock()
    
    #OnScreen Time of day clock###############################
def cornerClockDisplay():
    def updateCornerClock():
        cornerClock.config(text=back.getShortToday())
        root.after(1000, updateCornerClock)  # Update every second

    cornerClock = clockLabel(back.getShortToday(), None, int(sys.scn_h / 27))
    cornerClock.place(
        x=sys.scn_w / 2,
        y=sys.scn_h - sys.mainButton_h,
        width=sys.scn_w / 2,
        height=sys.scn_h / 8
    )
    cornerClock.pack(side=tk.RIGHT, anchor='sw')
    updateCornerClock()
    

    


    



####################################################################################################
# Start by showing the main menu screen
####################################################################################################
####################################################################################################
####################################################################################################
mainMenuScreen()
root.mainloop()
