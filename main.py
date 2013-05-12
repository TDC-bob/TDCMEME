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
import mizfile, logging, github
from os import listdir
from os.path import join
from _logging import mkLogger, logged
logger = mkLogger(__name__, logging.DEBUG )

mizPath1 = r"C:\Documents and Settings\owner\My Documents\BORIS\TDCMEME\missions\1.2.4\BenJee"
mizFiles = (join(mizPath1, file) for file in listdir(mizPath1) if file[-4:] == ".miz")

def main():
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
