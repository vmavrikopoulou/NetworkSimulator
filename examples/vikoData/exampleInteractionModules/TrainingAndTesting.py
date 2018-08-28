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
        
        elif self.lastTime < 23 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room1")

        elif self.lastTime < 25 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room2")
               
        #elif self.lastTime < 4  and time >= 4:
        #    self.sendMessage({"startTraining", label:"room2"})
            
        elif self.lastTime < 53 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room2")

        elif self.lastTime < 55 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room5")
        
        elif self.lastTime < 73 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room5")

        elif self.lastTime < 75 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room6")
        
        elif self.lastTime < 81 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room6")

        elif self.lastTime < 90 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room3")
        
        elif self.lastTime < 99 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room3")

        elif self.lastTime < 101 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room4")
        
        elif self.lastTime < 126 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room4")

        elif self.lastTime < 128 <= time:
            self.sendMessage("StartTraining")
            self.sendMessage("Room7")
        
        elif self.lastTime < 160 <= time:
            self.sendMessage("StopTraining")
            self.sendMessage("Room7")


    #first room layout
    # def tick(self, time):
    #     if time == 0:
    #         self.sendMessage("StartTraining")
    #         self.sendMessage("Room4")
        
    #     elif self.lastTime < 13 <= time:
    #         self.sendMessage("StopTraining")
    #         self.sendMessage("Room4")

    #     elif self.lastTime < 26 <= time:
    #         self.sendMessage("StartTraining")
    #         self.sendMessage("Room5")
               
    #     #elif self.lastTime < 4  and time >= 4:
    #     #    self.sendMessage({"startTraining", label:"room2"})
            
    #     elif self.lastTime < 27 <= time:
    #         self.sendMessage("StopTraining")
    #         self.sendMessage("Room5")

    #     elif self.lastTime < 29 <= time:
    #         self.sendMessage("StartTraining")
    #         self.sendMessage("Room3")
        
    #     elif self.lastTime < 70 <= time:
    #         self.sendMessage("StopTraining")
    #         self.sendMessage("Room3")

    #     elif self.lastTime < 73 <= time:
    #         self.sendMessage("StartTraining")
    #         self.sendMessage("Room2")
        
    #     elif self.lastTime < 94 <= time:
    #         self.sendMessage("StopTraining")
    #         self.sendMessage("Room2")

    #     elif self.lastTime < 97 <= time:
    #         self.sendMessage("StartTraining")
    #         self.sendMessage("Room1")
        
    #     elif self.lastTime < 109 <= time:
    #         self.sendMessage("StopTraining")
    #         self.sendMessage("Room1")


        self.lastTime = time
