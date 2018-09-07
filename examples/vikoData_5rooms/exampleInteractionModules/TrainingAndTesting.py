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
    # # first room layout
    def tick(self, time):
        if time == 0:
            self.sendMessage("StartTraining")
            self.sendMessage("Room1")
        
        elif self.lastTime < 14 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room1")

        elif self.lastTime < 16.5 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room2")
            
        elif self.lastTime < 36 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room2")

        elif self.lastTime < 38.5 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room3")
        
        elif self.lastTime < 77.5 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room3")

        elif self.lastTime < 80.5 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room4")
        
        elif self.lastTime < 92 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room4")

        elif self.lastTime < 95 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room5")
        
        elif self.lastTime < 110.8 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room5")

        elif self.lastTime < 115 <= time:
            self.sendMessage("StartLocalizing")


        self.lastTime = time
