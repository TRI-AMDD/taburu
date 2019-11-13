import abc
from monty.json import jsanitize


class Channel(abc.ABC):
    @abc.abstractmethod
    def publish(self, event):
        pass


class FileChannel(Channel):
    def __init__(self, filename):
        self._filename = filename

    def publish(self, event):
        data = jsanitize(event, strict=True)
        with open(self._filename, "a+") as f:
            f.write(data)


class KinesisChannel(Channel):
    def __init__(self):
        raise NotImplementedError("Kinesis channel not yet implemented")

    def publish(self, event):
        raise NotImplementedError("Kinesis channel not yet implemented")
