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
        
        elif self.lastTime < 34 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room1")

        elif self.lastTime < 36 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room2")
               
        #elif self.lastTime < 4  and time >= 4:
        #    self.sendMessage({"startTraining", label:"room2"})
            
        elif self.lastTime < 49 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room2")

        elif self.lastTime < 51 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room3")
        
        elif self.lastTime < 83 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room3")

        elif self.lastTime < 88 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room4")
        
        elif self.lastTime < 97 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room4")

        elif self.lastTime < 99 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room5")
        
        elif self.lastTime < 123 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room5")

        elif self.lastTime < 126 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room6")
        
        elif self.lastTime < 151 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room6")

        elif self.lastTime < 153 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room7")
        
        elif self.lastTime < 178 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room7")

        elif self.lastTime < 180 <= time:
            self.sendMessage("StartLocalizing")


        self.lastTime = time
