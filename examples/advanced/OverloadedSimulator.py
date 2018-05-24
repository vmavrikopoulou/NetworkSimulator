from simulator import Simulator
from simulator.util.Enums import MessageState


class CustomSimulator(Simulator):
    """
    This is a wrapper class to expose an API
    """
    
    def __init__(self):
        super().__init__()

    # overloaded
    def handleMessage(self, message, receiver):
        """
        This can be overridden to implement delays, topology, failures, etc.
        :param message:
        :param receiver:
        :return: MessageState.DELIVERED, MessageState.DELAYED, MessageState.FAILED
        """
        receiver.receiveMessage(message)
        return MessageState.DELIVERED