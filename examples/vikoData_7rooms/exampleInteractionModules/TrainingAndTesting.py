from simulator.simulatorBases.InteractionCore import InteractionCore


class TrainingAndTesting(InteractionCore):
    
    targetParameters = None
    lastTime = 0
    
    ###
    # The name is the "address" of the user that broadcasts the messages
    ###
    def __init__(self, name):
        super().__init__(name)
        
    # override

    #second roomlayout
    def tick(self, time):
        if time == 0:
            self.sendMessage("StartTraining")
            self.sendMessage("Room1")
        
        elif self.lastTime < 44.0 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room1")

        elif self.lastTime < 45.2 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room2")
            
        elif self.lastTime < 59.4 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room2")

        elif self.lastTime < 60.8 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room3")
        
        elif self.lastTime < 97.5 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room3")

        elif self.lastTime < 101.2 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room4")
        
        elif self.lastTime < 113.7 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room4")

        elif self.lastTime < 114 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room5")
        
        elif self.lastTime < 143.8 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room5")

        elif self.lastTime < 144 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room6")
        
        elif self.lastTime < 176.9 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room6")

        elif self.lastTime < 179.2 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room7")
        
        elif self.lastTime < 207.4 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room7")

        elif self.lastTime < 213 <= time:
            self.sendMessage("StartLocalizing")

        elif self.lastTime < 223 <= time:
            self.sendMessage("StopLocalizing")

        self.lastTime = time
