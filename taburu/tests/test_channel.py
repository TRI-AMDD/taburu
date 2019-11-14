#  Copyright (c) 2019 Toyota Research Institute.  All rights reserved.

import unittest
from monty.tempfile import ScratchDir


class FileChannelTest(unittest.TestCase):
    def test_subscribe(self):
        with ScratchDir('.'):
            fchannel = FileChannel("test.txt")



if __name__ == '__main__':
    unittest.main()
