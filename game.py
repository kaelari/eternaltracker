class game:
    fire = 0
    shadow = 0
    time = 0
    primal = 0
    justice = 0
    over = 3
    name = "unknown"
    def __init__(self): 
        fire = 0
        shadow = 0
        time = 0
        primal = 0
        justice = 0
        over = 3
        name = "Unknown"
        
    def endgame(self):
        win="won"
        if self.over == 1 :
            print ("we won the game")
        if self.over == 2 :
            print ("we lost the game")
            win = "lost";
            
        factions= ""
        if self.fire:
            factions="F"
        if self.shadow:
            factions+="S"
        if self.time:
            factions += "T"
        if self.primal:
            factions +="P"
        if self.justice:
            factions +="J"
            
        print (factions)
        f = open("log.txt", "a")
        f.write(win+","+factions+","+self.name +"\n")
        f.close()
        
    
