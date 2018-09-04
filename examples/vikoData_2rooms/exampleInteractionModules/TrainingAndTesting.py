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


    # map with 2 maps
    def tick(self, time):
        if time == 0:
            self.sendMessage("StartTraining")
            self.sendMessage("Room1")
        
        elif self.lastTime < 41.6 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room1")

        elif self.lastTime < 44 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room2")
            
        elif self.lastTime < 103 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room2")

        elif self.lastTime < 107 <= time:
            self.sendMessage("StartLocalizing")


        self.lastTime = time
