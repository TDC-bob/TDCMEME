#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     12/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from _logging import logged, mkLogger
import _slpp, logging
mkLogger(__name__,logging.DEBUG)

class Mission():

    @logged
    def __init__(self, path_to_mission_file):
        self.logger.info("instanciation d'un nouvel object mission: {}".format(path_to_mission_file))
        parser = _slpp.SLPP()
        with open(path_to_mission_file,mode="r",encoding="UTF-8") as file:
            self.raw_text = file.read()
        self.d = parser.decode(self.raw_text)
        print(len(self.d))

    @logged
    def __str__(self):
        self.logger.info("returning basic string info about mission's dictionnary")
        primary_keys = self.d.keys()
        rtn = list()
        for k in primary_keys:
            rtn.append(k)
            print(type(self.d[k]))
            if type(self.d[k]) == dict:
                rtn.append("\n".join(["\t\t{}".format(kk) for kk in self.d[k].keys()]))
            else:
                rtn.append("\t\t{}".format(self.d[k]))

        return "\n".join(rtn)

