import abc
from .event import ParametersAdded, MethodAdded
from .table import ParameterTable
from indexed import IndexedOrderedDict


class State(abc.ABC):
    @abc.abstractmethod
    def apply(self, event):
        pass


class uProjectState(State):
    def __init__(self):
        self.parameters = IndexedOrderedDict()
        self.methods = IndexedOrderedDict()

    def apply(self, event):
        if isinstance(event, ParametersAdded):
            if event.table_name in self.parameters:
                self.parameters[event.table_name].append(event.parameters)
            else:
                self.parameters[event.table_name] = ParameterTable(event.parameters)
        elif isinstance(event, MethodAdded):
            if self.methods.get(event.name) is None:
                self.methods[event.name] = event.parameter_indices
            else:
                print("Method name already exists")
                return False
        return True



