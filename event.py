import abc
from datetime import datetime
from monty.json import MSONable


class Event(abc.ABC):
    def __init__(self, time=None):
        self._time = time or datetime.utcnow().isoformat()


# TODO: more descriptive name, populate space?
class ParametersAdded(Event, MSONable, time=None):
    def __init__(self, table_name, parameters, time):
        self.table_name = table_name
        self.parameters = parameters
        super(Event, self).__init__(time)

    def as_dict(self):
        return {
            "table_name": self.table_name,
            "parameters": self.parameters,
            "time": self._time
        }


class MethodAdded(Event, MSONable):
    def __init__(self, name, parameter_indices, time=None):
        self.name = name
        self.parameter_indices = parameter_indices
        super(Event, self).__init__(time)

    def as_dict(self):
        return {
            "name": self.name,
            "parameters": self.parameter_indices,
            "time": self._time
        }

