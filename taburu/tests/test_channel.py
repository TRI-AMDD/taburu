#  Copyright (c) 2019 Toyota Research Institute.  All rights reserved.

import unittest
import json
import time
from multiprocessing.pool import ThreadPool
from monty.tempfile import ScratchDir
from taburu.channel import FileChannel


class FileChannelTest(unittest.TestCase):
    def test_subscribe(self):
        with ScratchDir('.'):
            with open("test.txt", 'w+') as f:
                f.write('\n'.join([json.dumps({"index":i}) for i in range(10)]))
            fchannel = FileChannel("test.txt")
            for n, obj in enumerate(fchannel.subscribe(iterations=0)):
                self.assertEqual(obj['index'], n)
            for n, obj in enumerate(fchannel.subscribe(iterations=2, poll_time=2)):
                self.assertEqual(obj['index'], n)

    @staticmethod
    def subscribe_to_channel(channel, iterations=None, poll_time=10):
        """Static method for executing channel subscriptions asyncronously"""
        return [obj for obj in channel.subscribe(iterations=iterations, poll_time=poll_time)]

    def test_async_subscribe(self):
        def dump_things(fname, objs):
            with open(fname, 'a+') as f:
                f.write('\n'.join([json.dumps(obj) for obj in objs]))

        with ScratchDir('.'):
            dump_things("test.txt", [{"index": i} for i in range(10)])
            pool = ThreadPool(processes=2)
            channel = FileChannel("test.txt")
            # Define the two threads
            channel_output = pool.apply_async(
                self.subscribe_to_channel, (channel, 2, 10)
            )
            time.sleep(10)
            pool.apply_async(dump_things, ("test.txt", [{"data": 10}]))
            self.assertEqual(channel_output.get()[-1]['data'], 10)


if __name__ == '__main__':
    unittest.main()
