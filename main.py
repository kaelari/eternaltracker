import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from game import game
import pytesseract

#haystack_image = cv.imread('allcolors.PNG', cv.IMREAD_UNCHANGED)
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
defeat_image = cv.imread('defeat.png', cv.IMREAD_UNCHANGED)
defeat_image = defeat_image[...,:3]


#result = cv.matchTemplate(haystack_image, needle_image, cv.TM_CCOEFF_NORMED)

#get best and worst match
#min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
#wincap = WindowCapture('allcolors.PNG ‎- Photos')
# wincap = WindowCapture('Eternal Card Game')
resources = WindowCapture('Eternal Card Game', 520, 40, 600, 70)
victory = WindowCapture('Eternal Card Game', 700, 10, 600, 100)
namewindow = WindowCapture('Eternal Card Game', 430, 10, 220, 30)

threshold = 0.8
loop_time = time()
thisgame = game()

while(True):

    # get an updated image of the game
    screenshot = resources.get_screenshot()
    screenshot2 = victory.get_screenshot()
    screenshot3 = namewindow.get_screenshot()
    
    cv.imshow('Computer Vision2', screenshot2)
    
    result = cv.matchTemplate(screenshot3, fire_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.fire == 0 :
        if max_val > threshold :
            print("Found Fire!")
            print("likelihood : %", max_val)
            thisgame.fire = 1
    
    result = cv.matchTemplate(screenshot, justice_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.justice == 0 :
        if max_val >threshold :
            print("Found Justice!")
            print("likelihood : %", max_val)
            thisgame.justice = 1
            
    result = cv.matchTemplate(screenshot, time_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.time == 0 :
        if max_val > threshold:
            print("Found Time!")
            print("likelihood : %", max_val)
            thisgame.time = 1
    result = cv.matchTemplate(screenshot, primal_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.primal == 0 :
        if max_val >threshold :
            print("Found Primal!")
            print("likelihood : %", max_val)
            thisgame.primal = 1
        
    result = cv.matchTemplate(screenshot, shadow_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
    if thisgame.shadow == 0 :
        if max_val >threshold:
            print("Found Shadow!")
            print("likelihood : %", max_val)
            thisgame.shadow=1
    if thisgame.over == 1:
        result = cv.matchTemplate(screenshot2, victory_image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
        if max_val < threshold :
            print ("We left the end game screen")
            thisgame.endgame()
            thisgame=game()
        
    if thisgame.over == 2:
        result = cv.matchTemplate(screenshot2, defeat_image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
        if max_val < threshold :
            print ("We left the end game screen")
            thisgame.endgame()
            thisgame=game()
    
    
    if thisgame.over == 0:
        custom_config = r'-c tessedit_char_whitelist=\ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 7  --oem 3 '
        gray = cv.cvtColor(screenshot3, cv.COLOR_BGR2GRAY)
        cv.imshow('Computer Vision3', gray)
        text = pytesseract.image_to_string(gray, config=custom_config)
        thisgame.name = text.rstrip()
        print ("name: "+text.rstrip())
        result = cv.matchTemplate(screenshot2, victory_image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
        if max_val > threshold :
            print ("Game has ended! we won!")
            thisgame.over = 1;
        result = cv.matchTemplate(screenshot2, defeat_image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result);
        if max_val > threshold :
            print ("Game has ended! we lost!")
            thisgame.over = 2;
        
        
    
    # debug the loop rate
    #print('FPS {}'.format(1 / (time() - loop_time)))
    #loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')



