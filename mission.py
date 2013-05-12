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

import _slpp, _logging, logging
_logging.mkLogger(__name__,logging.DEBUG)

class Mission():
    @logged
    def __init__(self, path_to_mission_file):
        parser = _slpp.SLPP()
