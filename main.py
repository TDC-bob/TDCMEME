# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Author:      Bob Daribouca
#
# Copyright:   (c) Bob Daribouca 2013
# Licence:     CC BY-NC-SA 3.0
#
#               Please refer to the "LICENSE" file distributed with the package,
#               or to http://creativecommons.org/licenses/by-nc-sa/3.0/
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import mizfile, logging, _slpp, filecmp, difflib, mission, os
from _logging import mkLogger, logged
logger = mkLogger(__name__, logging.INFO )

def main():
    wk_dir = os.getcwd()
    missions_in = os.path.join(wk_dir,"missions_in")
    missions_out = os.path.join(wk_dir, "missions_out")
    miz_files_in = (os.path.join(missions_in, file) for file in os.listdir(missions_in) if file[-4:] == ".miz")
    # run tests here
    '''
    SLPP test: in- & output of SLPP parsing should be *EXACTLY* the same
    '''
    SLPP_test(r"C:\Documents and Settings\owner\My Documents\BORIS\TDCMEME.git\slpp tests\mission",
            r"C:\Documents and Settings\owner\My Documents\BORIS\TDCMEME.git\slpp tests\output")

    # one test to rule them all:
    run_on_all_files(generate_context,miz_files_in)

def SLPP_test(file_in, file_out):
    '''
    Vérifie que le parser SLPP n'altère pas la table LUA qui lui est passée en
    entrée

    '''
    p = _slpp.SLPP()
    with open(file_out, mode="w", encoding="UTF-8") as _out:
        with open(file_in, encoding="UTF-8") as _in:
            dict_in = p.decode(_in.read())
            _out.write(p.encode(dict_in))

    with open(file_out, mode="r", encoding="UTF-8") as _out:
        dict_out = p.decode(_out.read())
    dicts_identical = (dict_in == dict_out)
    files_identical = (open(file_in).read() == open(file_out).read())
    print(files_identical)
    if not files_identical:
        with open(file_in) as f, open(file_out) as g:
            flines = f.readlines()
            glines = g.readlines()
            output = []
            for i in range(max(len(glines),len(flines))):
                if not glines[i] == flines[i]:
                    output.append("+ {}".format(glines[i]))
                    output.append("- {}".format(flines[i]))
        with open(os.path.join(os.path.dirname(file_in),"diff.txt"),mode="w") as diff_file:
            diff_file.writelines(output)

def generate_context(file):
    with mission.Mission(file):
        pass

def run_on_all_files(function, files):
    for file in files:
        print("running function {} on file {}".format(function.__name__,file))
        function(file)

if __name__ == '__main__':
    main()
