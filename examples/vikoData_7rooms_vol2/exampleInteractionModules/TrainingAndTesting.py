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
        
        elif self.lastTime < 110.0 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room1")

        elif self.lastTime < 111.2 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room2")
            
        elif self.lastTime < 149.8 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room2")

        elif self.lastTime < 150 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room3")
        
        elif self.lastTime < 251.2 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room3")

        elif self.lastTime < 253 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room4")
        
        elif self.lastTime < 301.2 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room4")

        elif self.lastTime < 302.8 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room5")
        
        elif self.lastTime < 441 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room5")

        elif self.lastTime < 442.6 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room6")
        
        elif self.lastTime < 561.4 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room6")

        elif self.lastTime < 564.6 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room7")
        
        elif self.lastTime < 665 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room7")

        elif self.lastTime < 666 <= time:
            self.sendMessage("StartLocalizing")

        elif self.lastTime < 680 <= time:
            self.sendMessage("StopLocalizing")

        self.lastTime = time
