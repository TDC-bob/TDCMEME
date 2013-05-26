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

import unittest, glob

from _logging._logging import mkLogger, logged, DEBUG, INFO
mkLogger(__name__, INFO)

if __name__ == '__main__':
    try:
        import nose
        nose.run()
    except ImportError:
        import unittest
        try:
            from . import test_ground_unit_resolve, tests_slpp
        except ImportError:
            import test_ground_unit_resolve, tests_slpp
        except KeyboardInterrupt:
            pass
        test_file_strings = glob.glob('test*.py')
        module_strings = [str[0:len(str)-3] for str in test_file_strings]
        suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str
                  in module_strings]
        testSuite = unittest.TestSuite(suites)
        text_runner = unittest.TextTestRunner().run(testSuite)
