#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     22/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import unittest, logging

try:
    import _logging
except ImportError:
    from . import _logging

class TestLoggingPackage(unittest.TestCase):

    def SetUp(self):
        pass

    def TearDown(self):
        pass

    def test_main_logger_init(self):
        logger = _logging.mkLogger("main")
        self.assertTrue(type(logger) == logging.Logger)


if __name__ == '__main__':
    unittest.main(verbosity=9)
