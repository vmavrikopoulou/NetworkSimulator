from simulator.core.SimulationCore import SimulationCore
from simulator.util.Enums import MessageState


class Simulator(SimulationCore):
    """
    This is a wrapper class to expose an API
    """
  
    # overloaded
    def handleMessage(self, message, receiver):
        """
        This can be overridden to implement delays, topology, failures, etc.
        :param message:
        :param receiver:
        :return:
        """
        receiver.receiveMessage(message)
        return MessageState.DELIVERED