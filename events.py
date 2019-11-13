import abc
from datetime import datetime
from monty.json import MSONable

class Event(abc.ABC):
    def __init__(self, time=None):
        self._time = time or datetime.utcnow().isoformat()


# TODO: more descriptive name, populate space?
class ParametersAdded(Event, MSONable, time=None):
    def __init__(self, table_name, parameters, time):
        self._table_name = table_name
        self._parameters = parameters
        super(Event, self).__init__(time)

    def as_dict(self):
        return {
            "table_name": self._table_name,
            "parameters": self._parameters,
            "time": self._time
        }


class MethodAdded(Event, MSONable):
    def __init__(self, name, parameter_names, time=None):
        self._name = name
        self._parameter_names = parameter_names
        super(Event, self).__init__(time)

    def as_dict(self):
        return {
            "name": self._name,
            "parameters": self._parameter_names,
            "time": self._time
        }

