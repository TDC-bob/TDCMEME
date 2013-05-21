#This file was originally generated by PyScripter's unitest wizard

import os, unittest
##import main
from _slpp import SLPP
from mission import Mission

##import _slpp
##import mission
##from ..slpp import SLPP
try:
    import Exceptions
except ImportError:
    pass

from _logging._logging import mkLogger, logged, DEBUG, INFO
mkLogger(__name__, INFO)

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gh1_SLPP_consistency_1(self):
        '''
        Verify that the SLPP parser outputs the EXACT same thing i's got
        (providing the mission file has not been changed)

        Fixes gh-1

        To run test, drop any number of *.miz files into the slpp tests directory
        '''
        try:
            miz_files = os.listdir("tests/slpp_tests")
        except (Exceptions.Error, FileNotFoundError):
            miz_files = os.listdir("slpp_tests")

        p = SLPP()
        for f in miz_files:
            try:
                file_out = os.path.normpath(os.path.join(os.getcwd(),"tests/slpp_tests/output"))
                if not f[-4:] == ".miz":
                    continue
                path_to_file = os.path.normpath(os.path.join(os.getcwd(),"tests/slpp_tests",f))
                with Mission(os.path.abspath(path_to_file)) as m:
                    path_to_mission_file = os.path.normpath(os.path.join(m.mizfile.temp_dir, "mission" ))
##                    file_in = os.path.join(os.getcwd(),"tests/slpp_tests/mission")
                    with open(file_out, mode="w", encoding="UTF-8") as _out:
                        with open(path_to_mission_file, encoding="UTF-8") as _in:
                            _out.write(p.encode(p.decode(_in.read())))
                    with open(path_to_mission_file) as f1, open(file_out) as f2:
                        self.assertTrue(f1.read() == f2.read())
            except (Exceptions.Error, FileNotFoundError):
                file_out = os.path.normpath(os.path.join(os.getcwd(),"slpp_tests/output"))
                if not f[-4:] == ".miz":
                    continue
                path_to_file = os.path.normpath(os.path.join(os.getcwd(),"slpp_tests",f))
                with Mission(os.path.abspath(path_to_file)) as m:
                    path_to_mission_file = os.path.normpath(os.path.join(m.mizfile.temp_dir, "mission" ))
##                    file_in = os.path.normpath(os.path.join(os.getcwd(),"slpp_tests/mission"))
                    with open(file_out, mode="w", encoding="UTF-8") as _out:
                        with open(path_to_mission_file, encoding="UTF-8") as _in:
                            _out.write(p.encode(p.decode(_in.read())))
                    with open(path_to_mission_file) as f1, open(file_out) as f2:
                        self.assertTrue(f1.read() == f2.read())

if __name__ == '__main__':
    unittest.main(verbosity=9)