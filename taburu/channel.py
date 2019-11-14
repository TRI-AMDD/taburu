import abc
from monty.json import jsanitize
import threading

# This should probably be on a per-file basis
CHANNEL_THREAD_LOCK = threading.Lock()


class Channel(abc.ABC):
    @abc.abstractmethod
    def publish(self, event):
        pass


class FileChannel(Channel):
    def __init__(self, filename):
        self._filename = filename

    def publish(self, event):
        data = jsanitize(event, strict=True)
        CHANNEL_THREAD_LOCK.acquire()
        with open(self._filename, "a+") as f:
            f.write(data)
        CHANNEL_THREAD_LOCK.release()

    def subscribe(self, poll_time=10):
        with open(self._filename, "r+") as f:
            while True:
                while f.tell():
                    print('Next')
                    yield f.next()





class KinesisChannel(Channel):
    def __init__(self):
        raise NotImplementedError("Kinesis channel not yet implemented")

    def publish(self, event):
        raise NotImplementedError("Kinesis channel not yet implemented")
