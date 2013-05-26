#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     26/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import unittest
import Exceptions
import mizfile
import glob

if os.path.exists("../missions"):
    root = "../missions/1.2.4"
else:
    root = "./missions/1.2.4"

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_instance(self):
        if os.getenv("TRAVIS") == 'true':
            raise SkipTest()
        m = mizfile.MizFile(os.path.join(root,"BenJee/MiG-29S - Abkhaz Fulcrums.miz"))
        m.check().decompact().recompact().delete_temp_dir()
        self.assertTrue(os.path.exists(os.path.join(root,"BenJee/TDCMEME/MiG-29S - Abkhaz Fulcrums.miz")))
        os.remove(os.path.join(root,"BenJee/TDCMEME/MiG-29S - Abkhaz Fulcrums.miz"))
        os.removedirs(os.path.join(root,"BenJee/TDCMEME"))

    def test_mizfile_check_bad_zip_file(self):
        if os.getenv("TRAVIS") == 'true':
            raise SkipTest()
        with self.assertRaises(Exceptions.InvalidMizFile):
            m = mizfile.MizFile(os.path.join(root,"INVALID/invalid.miz"))
            m.check()

    def test_mizfile_check_permission_errors(self):
        if os.getenv("TRAVIS") == 'true':
            raise SkipTest()
        with self.assertRaises(Exceptions.PermissionError):
            m = mizfile.MizFile(os.path.join(root,"INVALID"))
            m.check()

    def test_mizfile_file_does_no_exist(self):
        with self.assertRaises(Exceptions.FileDoesNotExist):
            m = mizfile.MizFile(os.path.join(root,"INVALID_CARIBOU"))
            m.check()

# TODO: check exception when TempDir can't be deleted
##    def test_mizfile_check_permission_errors(self):
##        if 'TRAVIS' in os.environ and os.environ['TRAVIS'] == '1':
##            raise SkipTest()
##        with self.assertRaises(Exceptions.Error):
##            m = mizfile.MizFile(os.path.join(root,"BenJee/MiG-29S - Abkhaz Fulcrums.miz"))
##            m.check().decompact()



if __name__ == '__main__':
    try:
        unittest.main(verbosity=9)
    except KeyboardInterrupt:
        pass