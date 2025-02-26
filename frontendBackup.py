import customtkinter as ctk
import systemVariables as sys
import backend as back
import time
from PIL import Image

# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")  # Match dark theme from original
ctk.set_default_color_theme("blue")  # Use built-in theme as base

# Initialize the main window
root = ctk.CTk()
root.geometry(f"{sys.scn_w}x{sys.scn_h}")
root.configure(fg_color=sys.cSecond)
back.clearTempLog()
root.resizable(False, False)

def clearScreen():
    for widget in root.winfo_children():
        widget.destroy()

# Header Setup
def updateHeader(vtext, boolIcons=True):
    global topHeader, settingsIconButton, homeIconButton
    
    topHeader = ctk.CTkFrame(root, fg_color=sys.cMain)
    topHeader_h = sys.scn_h // 8
    topHeader.place(x=0, y=0, width=sys.scn_w, height=topHeader_h)
    
    headerTitle = ctk.CTkLabel(topHeader, 
                             text=root.title(), 
                             fg_color=sys.cMain,
                             text_color=sys.cWhite,
                             font=('Lexend', int(sys.scn_h / 25), 'bold'),
                             anchor='w')
    headerTitle.place(x=10, y=0, width=sys.scn_w-20, height=topHeader_h)
    root.title(vtext)
    headerTitle.configure(text=vtext)

    icon_size = int(sys.scn_h / 10)
    if boolIcons:
        # Settings button
        settingsIconButton = ctk.CTkButton(
            topHeader,
            text="⚙️",
            command=settingsScreen,
            width=icon_size,
            height=icon_size,
            fg_color=sys.cMain,
            hover_color=sys.cSecond,
            font=('Arial', int(icon_size*0.6))
        )
        settingsIconButton.place(x=sys.scn_w - icon_size - 10, y=(topHeader_h - icon_size) / 2)
        # Home button
        homeIconButton = ctk.CTkButton(
            topHeader,
            text="🏠",
            command=mainMenuScreen,
            width=icon_size,
            height=icon_size,
            fg_color=sys.cMain,
            hover_color=sys.cSecond,
            font=('Arial', int(icon_size*0.6)))
        homeIconButton.place(x=sys.scn_w - 2*icon_size - 20, 
                            y=(topHeader_h - icon_size) / 2)

# Footer Setup
def updateFooter():
    global logoImageLabel
    try:
        logoImage = Image.open('images/PTC_Logo.png')
        logoImage = logoImage.resize((int(sys.scn_w), int(sys.scn_h//8)))
        logoImage = ctk.CTkImage(light_image=logoImage, dark_image=logoImage)
        
        logoImageLabel = ctk.CTkLabel(root, 
                                     image=logoImage, 
                                     text="",
                                     fg_color=sys.cMain)
        logoImageLabel.place(x=0, 
                            y=sys.scn_h - sys.scn_h//8, 
                            width=sys.scn_w, 
                            height=sys.scn_h//8)
    except Exception as e:
        print(f"Error loading logo: {e}")

# Button creation functions
def makeDefaultButton(vtext, vcommand):
    return ctk.CTkButton(root,
                        text=vtext,
                        font=('Lexend', int(sys.scn_h//25), 'bold'),
                        fg_color=sys.cMain,
                        text_color=sys.cWhite,
                        hover_color=sys.cSecond,
                        border_width=int(sys.scn_h//75),
                        command=vcommand)

def clockLabel(vtext, fontSize=int(sys.scn_w//10)):
    return ctk.CTkLabel(root,
                       text=vtext,
                       font=('Consolas', fontSize, 'bold'),
                       fg_color=sys.cMain,
                       text_color=sys.cWhite)

def makeColorButton(vtext, vcommand, vcolor):
    return ctk.CTkButton(root,
                        text=vtext,
                        font=('Lexend', int(sys.scn_h//25), 'bold'),
                        fg_color=vcolor,
                        text_color=sys.cWhite,
                        hover_color=vcolor,
                        border_width=int(sys.scn_h//75),
                        command=vcommand)

# Main Menu Screen
def mainMenuScreen():
    clearScreen()
    updateHeader('Main Menu')
    updateFooter()

    button_params = {
        'width': sys.mainButton_w,
        'height': sys.mainButton_h,
        'corner_radius': 10
    }
    
    y_positions = [
        sys.center_y - 2 * sys.mainButton_h,
        sys.center_y - sys.mainButton_h,
        sys.center_y,
        sys.center_y + sys.mainButton_h
    ]
    
    buttons = [
        ('Start A Race', raceSelectScreen),
        ('Race History', None),
        ('Calibrate', None),
        ('Setup Help', None)
    ]
    
    for (text, command), y in zip(buttons, y_positions):
        btn = makeDefaultButton(text, command)
        btn.place(x=sys.center_x - sys.mainButton_w//2, y=y, **button_params)
    
    cornerClockDisplay()

# Settings Screen
def settingsScreen():
    clearScreen()
    updateHeader('Settings')
    updateFooter()
    
    button_params = {
        'width': sys.scn_w,
        'height': sys.mainButton_h,
        'anchor': 'w'
    }
    
    options = [
        ('Units', None),
        ('Date/Time', None),
        ('Export Data', None),
        ('Import Data', None),
        ('Erase History', None)
    ]
    
    for i, (text, command) in enumerate(options):
        btn = makeDefaultButton(text, command)
        btn.place(x=0, y=sys.center_y - (3 - i) * sys.mainButton_h, **button_params)
    
    saveBtn = makeDefaultButton('Save Settings', None)
    saveBtn.place(x=0, y=sys.scn_h - sys.scn_h//8 - sys.mainButton_h,
                 width=sys.scn_w, height=sys.mainButton_h)
    
    cornerClockDisplay()

# Race Selection Screens
def raceSelectScreen():
    clearScreen()
    updateHeader('Race Select')
    updateFooter()

    distances = ['5K', '10K', 'Track', 'Custom']
    commands = [lambda: rScn('5K'), lambda: rScn('10K'), trackSetup, None]
    
    for i, (dist, cmd) in enumerate(zip(distances, commands)):
        btn = makeDefaultButton(dist, cmd)
        y_pos = sys.center_y - 2*sys.mainButton_h + i*(sys.mainButton_h*1.2)
        btn.place(x=sys.center_x - sys.mainButton_w//2,
                 y=y_pos,
                 width=sys.mainButton_w,
                 height=sys.mainButton_h)
    
    cornerClockDisplay()

# Race Screen
def rScn(distance):
    print(f"Race selected: {distance}")

def trackSetup():
    print("Track setup selected")

# Timer Functions
def startTimer():
    clearScreen()
    updateHeader('Timer Start', False)
    updateFooter()
    
    startBtn = makeColorButton(f'BEGIN {sys.runDistance} RACE', 
                              lambda: timerScreen(), 
                              'green')
    startBtn.place(x=0, y=sys.scn_h//8, 
                  width=sys.scn_w, 
                  height=sys.scn_h*0.75 - sys.scn_h//8)
    
    cancelBtn = makeDefaultButton('Cancel', mainMenuScreen)
    cancelBtn.place(x=0, y=sys.scn_h - sys.scn_h//8 - sys.scn_h//8,
                   width=sys.scn_w, height=sys.scn_h//8)
    
    cornerClockDisplay()

def updateClock():
    if back.timerRunning:
        displayClock.configure(text=back.rawTimeConvert())
        root.after(1, updateClock)
    else:
        displayClock.configure(text=back.rawTimeConvertOther(back.finishTime))

def timerButtons(vOn):
    if vOn:
        lapBtn = makeDefaultButton('Lap', back.lap)
        lapBtn.place(x=0, y=sys.scn_h - sys.scn_h//8 - sys.mainButton_h*1.5,
                    width=sys.scn_w//1.5, height=sys.mainButton_h*1.5)
        
        stopBtn = makeColorButton('Stop', 
                                 lambda: back.stopButtonPressed(timerScreen(False)), 
                                 'red')
        stopBtn.place(x=sys.scn_w//1.5, y=sys.scn_h - sys.scn_h//8 - sys.mainButton_h*1.5,
                     width=sys.scn_w//3, height=sys.mainButton_h*1.5)
    else:
        saveBtn = makeDefaultButton('Save', 
                                   lambda: back.saveButtonPressed(mainMenuScreen()))
        saveBtn.place(x=0, y=sys.scn_h - sys.scn_h//8 - sys.mainButton_h*1.5,
                      width=sys.scn_w, height=sys.mainButton_h*1.5)

def timerScreen(vTimerOn=True):
    global displayClock
    clearScreen()
    if vTimerOn:
        back.startTimer()
        
    updateHeader(f'{sys.runDistance} In Progress', False)
    updateFooter()
    
    displayClock = clockLabel(back.elapsedTime, int(sys.scn_w//10))
    displayClock.place(x=0, y=sys.center_y - 2.5*sys.mainButton_h,
                      width=sys.scn_w, height=sys.mainButton_h*2)
    
    timerButtons(vTimerOn)
    updateClock()
    cornerClockDisplay()

# Clock Display
def cornerClockDisplay():
    def updateCornerClock():
        cornerClock.configure(text=back.getShortToday())
        root.after(1000, updateCornerClock)
    
    cornerClock = clockLabel(back.getShortToday(), int(sys.scn_h//27))
    cornerClock.place(x=sys.scn_w//2, y=sys.scn_h - sys.mainButton_h,
                     width=sys.scn_w//2, height=sys.scn_h//8)
    updateCornerClock()

# Initialize and run
mainMenuScreen()
root.mainloop()