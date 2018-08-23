import uuid

class EventBus:
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.topics = {}
        self.subscriberIds = {}
    
    def subscribe(self, topic: object, callback: object) -> object:
        if topic not in self.topics:
            self.topics[topic] = {}
        
        subscriptionId = str(uuid.uuid4())
        self.subscriberIds[subscriptionId] = topic
        self.topics[topic][subscriptionId] = callback
        
        return subscriptionId
    
    def emit(self, topic, data=True):
        if topic in self.topics:
            for subscriptionId in self.topics[topic]:
                self.topics[topic][subscriptionId](data)
    
    def unsubscribe(self, subscriptionId):
        if subscriptionId is None:
            return
        
        if subscriptionId in self.subscriberIds:
            topic = self.subscriberIds[subscriptionId]
            if topic in self.topics:
                self.topics[topic].pop(subscriptionId)
            
            self.subscriberIds.pop(subscriptionId)
        else:
            print("ERROR: BluenetEventBus: Subscription ID ", subscriptionId, " cannot be found.")


    def destroy(self):
        self.topics = {}
        self.subscriberIds = {}
