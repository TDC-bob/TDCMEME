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
import mizfile, logging, slpp, _slpp, filecmp, difflib
from os import listdir
from os.path import join
from _logging import mkLogger, logged
logger = mkLogger(__name__, logging.INFO )

mizPath1 = r"C:\Documents and Settings\owner\My Documents\BORIS\TDCMEMEv2.git\missions\1.2.4\BenJee"
mizFiles = (join(mizPath1, file) for file in listdir(mizPath1) if file[-4:] == ".miz")

testMissionFile1 = r"C:\Documents and Settings\owner\My Documents\BORIS\TDCMEMEv2.git\missions\1.2.4\BenJee\mission1"
testMissionFile2 = r"C:\Documents and Settings\owner\My Documents\BORIS\TDCMEMEv2.git\missions\1.2.4\BenJee\mission2"
testMissionFile3 = r"C:\Documents and Settings\owner\My Documents\BORIS\TDCMEMEv2.git\missions\1.2.4\BenJee\mission3"
testMissionFileWrite = r"C:\Documents and Settings\owner\My Documents\BORIS\TDCMEMEv2.git\missions\1.2.4\BenJee\mission_out"
testMissionDiff =r"C:\Documents and Settings\owner\My Documents\BORIS\TDCMEMEv2.git\missions\1.2.4\BenJee\mission_diff.txt"

def main():
    p = _slpp.SLPP()

    with open(testMissionFileWrite, mode="w", encoding="UTF-8") as file_out:
        with open(testMissionFile3, encoding="UTF-8") as file_in:
            dict_in = p.decode(file_in.read())
            file_out.write(p.encode(dict_in))

    with open(testMissionFileWrite, mode="r", encoding="UTF-8") as file_out:
        dict_out = p.decode(file_out.read())

    print(dict_in == dict_out)
    return
    # Build files list
    logger.info("Building sample mission files list")
    for file in mizFiles:
        logger.debug("".join(["Found files: ", file]))
        instance = mizfile.MizFile(file)
        instance.check()
        instance.decompact()

##    t = mizfile.MizFile(mizFile1, "tmp")

if __name__ == '__main__':
    main()
