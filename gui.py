from tkinter import *
from game import game
import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from game import game



root = Tk()
root.title("Kael's Tracker")
root.geometry('450x200')
label = Label(root, text="Kael's tracker version 0.0.1 running")
label.pack()
def submitreport(won, fire, shadow, time, primal, justice, name, comments ):
    global thisgame
    win="won"
    if won == 1 :
        print ("we won the game")
    if won == 2 :
        print ("we lost the game")
        win = "lost";
            
    factions= ""
    if fire:
        factions="F"
    if shadow:
        factions+="S"
    if time:
        factions += "T"
    if primal:
        factions +="P"
    if justice:
        factions +="J"
            
    print (factions)
    f = open("log.txt", "a")
    f.write(win+","+factions+","+name +","+comments+"\n")
    f.close()
    global report
    report.destroy()
    thisgame = game()
    
def openreport():
    global report
    global thisgame
    global fire, shadow, time, justice, primal, won
    report=Toplevel()
    report.lift()
    report.attributes("-topmost", True)
    myButton = Button(report, text="Save!", command=lambda: submitreport(won.get(), fire.get(), shadow.get(), time.get(), primal.get(), justice.get(), usernameEntry.get(), commentEntry.get()) )
    myButton.grid(row=10, column=0, columnspan=10)
    winLabel = Label(report, text="Win?")
    winLabel.grid(row=0, column=0)
    
    
    won = IntVar(value=thisgame.over)
    
    wincheckbox = Checkbutton(report, variable=won, onvalue=1, offvalue=2)
    wincheckbox.grid(row=0, column=1)

    usernameLabel = Label(report, text="Opponent")
    usernameLabel.grid(row=1, column=0)

    usernameEntry = Entry(report, width=25)
    usernameEntry.grid(row=1, column=1, columnspan=10)
    
    fire = IntVar(value=thisgame.fire)
    shadow = IntVar(value=thisgame.shadow)
    time = IntVar(value=thisgame.time)
    justice = IntVar(value=thisgame.justice)
    primal = IntVar(value=thisgame.primal)


    firecheckbox = Checkbutton(report, text='Fire',variable=fire, onvalue=1, offvalue=0)
    firecheckbox.grid(row=2, column=1)
    shadowcheckbox = Checkbutton(report, text='Shadow',variable=shadow, onvalue=1, offvalue=0)
    shadowcheckbox.grid(row=2, column=2)
    timecheckbox = Checkbutton(report, text='Time',variable=time, onvalue=1, offvalue=0)
    timecheckbox.grid(row=2, column=3)
    justicecheckbox = Checkbutton(report, text='Justice',variable=justice, onvalue=1, offvalue=0)
    justicecheckbox.grid(row=2, column=4)
    primalcheckbox = Checkbutton(report, text='Primal',variable=primal, onvalue=1, offvalue=0)
    primalcheckbox.grid(row=2, column=5)
    commentLabel = Label(report, text="comments")
    commentLabel.grid(row=3, column=0)

    commentEntry = Entry(report, width=25)
    commentEntry.grid(row=3, column=1, columnspan=10)
    


fire_image = cv.imread('fire.png', cv.IMREAD_UNCHANGED)
fire_image = fire_image[...,:3]
justice_image = cv.imread('justice.png', cv.IMREAD_UNCHANGED)
justice_image = justice_image[...,:3]
time_image = cv.imread('time.png', cv.IMREAD_UNCHANGED)
time_image = time_image[...,:3]
primal_image = cv.imread('primal.png', cv.IMREAD_UNCHANGED)
primal_image = primal_image[...,:3]
shadow_image = cv.imread('shadow.png', cv.IMREAD_UNCHANGED)
shadow_image = shadow_image[...,:3]

victory_image = cv.imread('victory.png', cv.IMREAD_UNCHANGED)
victory_image = victory_image[...,:3]
defeat_image = cv.imread('Defeat2.png', cv.IMREAD_UNCHANGED)
defeat_image = defeat_image[...,:3]


#result = cv.matchTemplate(haystack_image, needle_image, cv.TM_CCOEFF_NORMED)

#get best and worst match
#min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
#wincap = WindowCapture('allcolors.PNG ‎- Photos')
# wincap = WindowCapture('Eternal Card Game')
resources = WindowCapture('Eternal Card Game', 520, 40, 600, 70)
victory = WindowCapture('Eternal Card Game', 700, 10, 600, 100)
#namewindow = WindowCapture('Eternal Card Game', 430, 10, 220, 30)

threshold = 0.8
loop_time = time()
global thisgame
thisgame = game()

def runcheck():
    global thisgame
    # get an updated image of the game
    screenshot = resources.get_screenshot()
    screenshot2 = victory.get_screenshot()
    
    result = cv.matchTemplate(screenshot, fire_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.fire == 0 :
        if max_val > threshold :
            print("Found Fire!")
            print("likelihood : %", max_val)
            thisgame.fire = 1
            if thisgame.over == 3 :
                thisgame.over=0
    
    result = cv.matchTemplate(screenshot, justice_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.justice == 0 :
        if max_val >threshold :
            print("Found Justice!")
            print("likelihood : %", max_val)
            thisgame.justice = 1
            if thisgame.over == 3 :
                thisgame.over=0
    
            
    result = cv.matchTemplate(screenshot, time_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.time == 0 :
        if max_val > threshold:
            print("Found Time!")
            print("likelihood : %", max_val)
            thisgame.time = 1
            if thisgame.over == 3 :
                thisgame.over=0
    
    result = cv.matchTemplate(screenshot, primal_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.primal == 0 :
        if max_val >threshold :
            print("Found Primal!")
            print("likelihood : %", max_val)
            thisgame.primal = 1
            if thisgame.over == 3 :
                thisgame.over=0
    
        
    result = cv.matchTemplate(screenshot, shadow_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.shadow == 0 :
        if max_val >threshold:
            print("Found Shadow!")
            print("likelihood : %", max_val)
            thisgame.shadow=1
            if thisgame.over == 3 :
                thisgame.over=0
    
    #if thisgame.over == 1:
        #result = cv.matchTemplate(screenshot2, victory_image, cv.TM_CCOEFF_NORMED)
        #min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
        #if max_val < threshold :
            #print ("We left the end game screen")
            #thisgame.endgame()
            #thisgame=game()
        
    #if thisgame.over == 2:
        #result = cv.matchTemplate(screenshot2, defeat_image, cv.TM_CCOEFF_NORMED)
        #min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
        #if max_val < threshold :
            #print ("We left the end game screen")
            #thisgame.endgame()
            #thisgame=game()
    
    
    if thisgame.over == 0:
        result = cv.matchTemplate(screenshot2, victory_image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
        if max_val > 0.9 :
            print ("Game has ended! we won!"+str(max_val))
            thisgame.over = 1;
            openreport()
        result = cv.matchTemplate(screenshot2, defeat_image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
        if max_val > 0.9 :
            print ("Game has ended! we lost!"+str(max_val))
            thisgame.over = 2;
            openreport()
        else :
            print (max_val);
    root.after(1000, runcheck)


root.after(0, runcheck)
root.mainloop()

