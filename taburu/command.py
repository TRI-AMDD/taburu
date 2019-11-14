from .state import uProjectState
from .event import Event, ParametersAdded, MethodAdded
from monty.json import MSONable


class AddParameterCommanded(ParametersAdded):
    """The event schema is the same aside from the name"""
    pass


class AddMethodCommanded(Event, MSONable):
    """Event schema is the same except with names instead of params"""
    def __init__(self, name, parameter_names, time=None):
        self.name = name
        self.parameter_names = parameter_names
        super(AddMethodCommanded, self).__init__(time)


class uProjectCommandProcessor(object):
    def __init__(self, input_channel, output_channel=None,
                 state=None):
        self.state = state or uProjectState()
        self.input_channel = input_channel
        self.output_channel = output_channel

    def publish(self, event):
        self.output_channel.publish(event)

    def process_command(self, command):
        if isinstance(command, AddParameterCommanded):
            parameters_added = ParametersAdded(command.table_name,
                                               command.parameters)
            if self.state.apply(parameters_added):
                self.publish(parameters_added)
        if isinstance(command, AddMethodCommanded):
            # look for methods in state
            try:
                state_parameter_names = self.state.parameters.keys()
                parameter_indices = tuple(
                    [state_parameter_names.index(parameter_name)
                     for parameter_name in command.parameter_names]
                )
            except ValueError as e:
                print("Parameter name mismatch: {}".format(e))
                return False
            method_added = MethodAdded(command.name, tuple(parameter_indices))
            if self.state.apply(method_added):
                self.publish(method_added)
        return True

    def run(self):
        for command in self.input_channel.subscribe():
            self.process_command(command)
