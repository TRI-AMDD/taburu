from .state import uProjectState
from .event import Event


def AddParameterCommanded(Event):

class uProjectCommandProcessor(object):
    def __init__(self, input_channel, output_channel=None,
                 initial_state=None):
        self.state = initial_state or uProjectState()
        self.input_channel = input_channel
        self.output_channel = output_channel

    def process_command(self, command):
        if