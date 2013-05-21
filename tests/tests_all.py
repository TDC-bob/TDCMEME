#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     21/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import unittest, test_ground_unit_resolve

from _logging._logging import mkLogger, logged, DEBUG, INFO
mkLogger(__name__, INFO)
import glob

try:
    import nose
    nose.run()
except ImportError:
    test_file_strings = glob.glob('test*.py')
    module_strings = [str[0:len(str)-3] for str in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str
              in module_strings]
    testSuite = unittest.TestSuite(suites)
    text_runner = unittest.TextTestRunner().run(testSuite)
