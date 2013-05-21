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

import unittest
##import main
import _slpp
import mission
##from ..slpp import SLPP
import os
import campaign.conflict as conflict
from campaign.ground_unit import GroundUnit
from _logging._logging import mkLogger, logged, DEBUG, INFO
mkLogger(__name__, DEBUG)

T54 = {
    "name":"T54",
    "role":"assault",
    "weight": "medium",
    "unit_type": "vehicle",
    "against": {"light":80,"medium":60,"heavy":40},
    "division":None,
    "speed_on_map":1,
    "speed_on_ground":4,
    "unit_range": 0,
    "fuel": 4,
    "ammo": 4,
    "moral": 10,
    "aggro": 2,
    "size": 6,
    "cost_to_buy": 50,
    "max_size": 6
    }
T80 = {
    "name":"T80",
    "role":"assault",
    "weight": "heavy",
    "unit_type": "vehicle",
    "against": {"light":80,"medium":70,"heavy":60},
    "division":None,
    "speed_on_map":1,
    "speed_on_ground":3,
    "unit_range": 0,
    "fuel": 4,
    "ammo": 4,
    "moral": 10,
    "aggro": 2,
    "size": 4,
    "cost_to_buy": 80,
    "max_size": 4
}
M16 = {
    "name":"M16",
    "role":"assault",
    "weight": "light",
    "unit_type": "infantry",
    "against": {"light":80,"medium":40,"heavy":20},
    "division":None,
    "speed_on_map":1,
    "speed_on_ground":2,
    "unit_range": 0,
    "fuel": 8,
    "ammo": 4,
    "moral": 10,
    "aggro": 2,
    "size": 16,
    "cost_to_buy": 10,
    "max_size": 16
}

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skip("temporary skip")
    def test_ground_unit_flee_speed(self):
        '''
        '''
        unit1 = GroundUnit(T54)
        unit2 = GroundUnit(T80)
        print("Base odds: ")
        unit1.flee(unit2)
        print("\n")
        print("testing speed_on_ground")
        for x in range(1,10):
            unit1.speed_on_ground = x
##            print("unit1 speed: {}".format(unit1.speed_on_ground))
            print(unit1.flee(unit2))

    def test_ground_unit_conflict(self):
        wins = {"unit1":0,"unit2":0,"pars":0}
        for x in range(1,100000):
            unit1 = GroundUnit(T54)
            unit2 = GroundUnit(T80)
            unit1.name = "unit1"
            unit2.name = "unit2"
            winner = conflict.resolve(unit1,unit2)
            if winner:
                wins[winner.name] += 1
            else:
                wins["pars"] += 1
        print("RESULTS:\nWin 1: {}\nWin 2:{}\nPars:{}".format(wins["unit1"],wins["unit2"],wins["pars"]))
##        if winner:
##            print("Winner: {}".format(winner.name))
##        else:
##            print("Both units fled")


def main():
    pass

if __name__ == '__main__':
    unittest.main(verbosity=9)
