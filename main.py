# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     10/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# coding=utf-8
import mizfile, logging, _slpp, filecmp, difflib, mission, os
from _logging import mkLogger, logged
logger = mkLogger(__name__, logging.INFO )

def main():
    wk_dir = os.getcwd()
    missions_in = os.path.join(wk_dir,"missions_in")
    missions_out = os.path.join(wk_dir, "missions_out")
    miz_files_in = (os.path.join(missions_in, file) for file in os.listdir(missions_in) if file[-4:] == ".miz")
    # run tests here

    # one test to rule them all:
##    for file_path in miz_files_in:
##        file_path = file_path.replace("\\","\\\\")
##        print(file_path)
    run_on_all_files(generate_context,miz_files_in)

def SLPP_test(file_in, file_out):
    '''
    Vérifie que le parser SLPP n'altère pas la table LUA qui lui est passée en
    entrée

    BUGGED: cfr. gh-1
    '''
    p = _slpp.SLPP()
    with open(file_out, mode="w", encoding="UTF-8") as _out:
        with open(file_in, encoding="UTF-8") as _in:
            dict_in = p.decode(_in.read())
            _out.write(p.encode(dict_in))

    with open(file_out, mode="r", encoding="UTF-8") as _out:
        dict_out = p.decode(_out.read())

    print(dict_in == dict_out)

def generate_context(file):
    with mission.Mission(file):
        pass

def run_on_all_files(function, files):
    for file in files:
        print("running function {} on file {}".format(function.__name__,file))
        function(file)

if __name__ == '__main__':
    main()
