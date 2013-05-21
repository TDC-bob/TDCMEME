#This file was originally generated by PyScripter's unitest wizard

import unittest
##import main
import _slpp
import mission
##from ..slpp import SLPP
import os
from _logging._logging import mkLogger, logged, DEBUG, INFO
mkLogger(__name__, INFO)

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gh1_SLPP_consistency_1(self):
        '''
        Verifies that the SLPP parser outputs the EXACT same output, providing
        the mission file has not been changed

        Fixes gh-1

        To run test, drop any number of *.miz files into the slpp tests directory
        '''
        miz_files = os.listdir("tests/slpp_tests")
        file_out = os.path.join(os.getcwd(),"slpp_tests/output")
        p = _slpp.SLPP()
        for f in miz_files:
            if not f[-4:] == ".miz":
                continue
            path_to_file = os.path.normpath(os.path.join(os.getcwd(),"tests/slpp_tests",f))
            with mission.Mission(os.path.abspath(path_to_file)) as m:
                path_to_mission_file = os.path.normpath(os.path.join(m.mizfile.temp_dir, "mission" ))
                file_in = os.path.join(os.getcwd(),"tests/slpp_tests/mission")
                with open(file_out, mode="w", encoding="UTF-8") as _out:
                    with open(file_in, encoding="UTF-8") as _in:
                        _out.write(p.encode(p.decode(_in.read())))
                with open(file_in) as f1, open(file_out) as f2:
                    self.assertTrue(f1.read() == f2.read())



if __name__ == '__main__':
    unittest.main()
