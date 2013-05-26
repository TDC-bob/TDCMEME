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

import unittest, os

from campaign import conflict
from campaign.ground_unit import GroundUnit

from _logging._logging import mkLogger, logged, DEBUG, INFO, WARN
logger=mkLogger(__name__, INFO, "tests.log")

number_of_tests_to_run = 10

T54 = {
    "name":"T54",
    "role":"assault",
    "weight": "medium",
    "unit_type": "vehicle",
    "against": {"light":75,"medium":50,"heavy":25},
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
    "against": {"light":60,"medium":30,"heavy":10},
    "division":None,
    "speed_on_map":1,
    "speed_on_ground":2,
    "unit_range": 0,
    "fuel": 8,
    "ammo": 4,
    "moral": 10,
    "aggro": 2,
    "size": 8,
    "cost_to_buy": 10,
    "max_size": 8
}
Jeep = {
    "name":"Jeep",
    "role":"recce",
    "weight": "light",
    "unit_type": "vehicle",
    "against": {"light":20,"medium":5,"heavy":0},
    "division":None,
    "speed_on_map":2,
    "speed_on_ground":8,
    "unit_range": 0,
    "fuel": 4,
    "ammo": 2,
    "moral": 10,
    "aggro": 0,
    "size": 4,
    "cost_to_buy": 25,
    "max_size": 4
}

unit_list = [Jeep,M16,T54,T80]

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

##    @unittest.skip("temporary skip")
    def test_ground_unit_unbalanced_conflict_speed(self):
        '''
        '''
        logger.info("testing speed modifications")
        for u1, u2 in [(u,u) for u in unit_list]:
##            number_of_tests_to_run = 1000
            for mod in [1,0.9,0.8,0.7,0.6,0.5]:
                wins = {}
                logger.info("unit2.speed * {}".format(mod))
                if os.getenv("TRAVIS") == 'true':
                    print("outputin' something to let Travis know we're not dead (yet)")
                for x in range(1,number_of_tests_to_run+1):
                    unit1 = GroundUnit(u1)
                    unit1.name = "{}_1".format(unit1.name)
                    unit2 = GroundUnit(u2)
                    unit2.name = "{}_2".format(unit2.name)
                    unit2.speed_on_ground *= mod
                    resolve_conflict(wins,unit1,unit2)
                show_results(wins,unit1,unit2)

##    @unittest.skip("temporary skip")
    def test_ground_unit_unbalanced_conflict_moral(self):
        '''
        '''
        logger.info("testing moral modifications")
        for u1, u2 in [(u,u) for u in unit_list]:
##            number_of_tests_to_run = 1000
            for mod in [1,0.9,0.8,0.7,0.6,0.5]:
                wins = {}
                logger.info("unit2.moral * {}".format(mod))
                if os.getenv("TRAVIS") == 'true':
                    print("outputin' something to let Travis know we're not dead (yet)")
                for x in range(1,number_of_tests_to_run+1):
                    unit1 = GroundUnit(u1)
                    unit1.name = "{}_1".format(unit1.name)
                    unit2 = GroundUnit(u2)
                    unit2.name = "{}_2".format(unit2.name)
                    unit2.moral *= mod
                    resolve_conflict(wins,unit1,unit2)
                show_results(wins,unit1,unit2)

##    @unittest.skip("temporary skip")
    def test_ground_unit_unbalanced_conflict_size(self):
        '''
        '''
        logger.info("testing size modifications")
        for u1, u2 in [(u,u) for u in unit_list]:
##            number_of_tests_to_run =1000
            for mod in [1,0.9,0.8,0.7,0.6,0.5]:
                if os.getenv("TRAVIS") == 'true':
                    print("outputin' something to let Travis know we're not dead (yet)")
                wins = {}
                logger.info("unit2.size * {}".format(mod))
                for x in range(1,number_of_tests_to_run+1):
                    unit1 = GroundUnit(u1)
                    unit1.name = "{}_1".format(unit1.name)
                    unit2 = GroundUnit(u2)
                    unit2.name = "{}_2".format(unit2.name)
                    unit2.size *= mod
                    resolve_conflict(wins,unit1,unit2)
                show_results(wins,unit1,unit2)
##            self.assertGreater(wins[unit2.name], 0, "Unit 2 must have been winning at least one round")
##            self.assertLess(wins[unit2.name], wins[unit1.name]/2, "Unit 2 can't win more than 1/3 of the rounds with half its size")

##    @unittest.skip("temporary skip")
    def test_ground_unit_balanced_conflict_same_units(self):
        '''
        '''
        logger.info("same units")
        for u1, u2 in [(u,u) for u in unit_list]:
            if os.getenv("TRAVIS") == 'true':
                print("outputin' something to let Travis know we're not dead (yet)")
            wins = {}
##            number_of_tests_to_run = 1000 # ne pas toucher !
            for x in range(1,number_of_tests_to_run+1):
                unit1 = GroundUnit(u1)
                unit1.name = "{}_1".format(unit1.name)
                unit2 = GroundUnit(u2)
                unit2.name = "{}_2".format(unit2.name)
                resolve_conflict(wins,unit1,unit2)
            show_results(wins,unit1,unit2)

##    @unittest.skip("temporary skip")
    def test_ground_unit_balanced_conflict_different_units(self):
        '''
        '''
        logger.info("different units")
        for u1 in [u for u  in unit_list]:
            for u2 in  [u for u in reversed(unit_list)]:
                if os.getenv("TRAVIS") == 'true':
                    print("outputin' something to let Travis know we're not dead (yet)")
                wins = {}
##                number_of_tests_to_run = 1000 # ne pas toucher !
                for x in range(1,number_of_tests_to_run+1):
                    unit1 = GroundUnit(u1)
                    unit1.name = "{}_1".format(unit1.name)
                    unit2 = GroundUnit(u2)
                    unit2.name = "{}_2".format(unit2.name)
                    resolve_conflict(wins,unit1,unit2)
                show_results(wins,unit1,unit2)

    @unittest.skip("temporary skip")
    def test_ground_unit_manual_tinkering(self):
        '''
        '''
        logger.info("manual testing")
        u1 = T54
        u2 = T80
        wins = {}
        if os.getenv("TRAVIS") == 'true':
            print("outputin' something to let Travis know we're not dead (yet)")
##        number_of_tests_to_run = 100
##        for u1, u2 in [(u,u) for u in unit_list]:
        for x in range(1,number_of_tests_to_run+1):
            unit1 = GroundUnit(u1)
            unit1.name = "{}_1".format(unit1.name)
            unit2 = GroundUnit(u2)
            unit2.name = "{}_2".format(unit2.name)
##            unit2.size *= 0.5
            resolve_conflict(wins, unit1, unit2)

        show_results(wins,unit1,unit2)

def show_results(wins,unit1,unit2):
    logger.info("RESULTS:\n{}\tWins: {}\tDestroyed: {}\tFled: {}\n{}\tWins: {}\tDestroyed: {}\tFled: {}\n\n".format(
                unit1.name, wins[unit1.name]["wins"], wins[unit1.name]["destroyed"], wins[unit1.name]["fled"],
                unit2.name, wins[unit2.name]["wins"], wins[unit2.name]["destroyed"], wins[unit2.name]["fled"]
                ))

def resolve_conflict(wins,unit1,unit2):
    try:
        wins[unit1.name]
    except KeyError:
        wins[unit1.name] = {"wins":0,"destroyed":0,"fled":0}
        wins[unit2.name] = {"wins":0,"destroyed":0,"fled":0}
    c = conflict.Conflict(unit1,unit2)
    winner, fled, destroyed = c.resolve()
    for w in winner:
        wins[w.name]["wins"] += 1
    for f in fled:
        wins[f.name]["fled"] += 1
    for d in destroyed:
        wins[d.name]["destroyed"] += 1

if __name__ == '__main__':
    try:
        unittest.main(verbosity=9)
    except KeyboardInterrupt:
        pass
