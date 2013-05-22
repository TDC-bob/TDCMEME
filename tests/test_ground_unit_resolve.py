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

import unittest, os

from campaign import conflict
from campaign.ground_unit import GroundUnit

from _logging._logging import mkLogger, logged, DEBUG, INFO
mkLogger(__name__, INFO)

T54 = {
    "name":"T54",
    "role":"assault",
    "weight": "medium",
    "unit_type": "vehicle",
    "against": {"light":80,"medium":60,"heavy":30},
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
    "against": {"light":90,"medium":70,"heavy":60},
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

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

##    @unittest.skip("temporary skip")
    def test_ground_unit_flee_speed(self):
        '''
        Testing flee against speed
        '''
        unit1 = GroundUnit(Jeep)
        unit2 = GroundUnit(T80)
##        print("Base odds: ")
        unit1.flee(unit2)
##        print("\n")
##        print("testing speed_on_ground")
        for x in range(1,10):
            unit1.speed_on_ground = x
##            print("unit1 speed: {}".format(unit1.speed_on_ground))
            print("unit1 speed: {}\tUnit fled: {}".format(unit1.speed_on_ground,unit1.flee(unit2)))

    def test_ground_unit_balanced_conflict(self):
        '''
        Testing conflict resolution
        '''
        for u1, u2 in [
            [Jeep,Jeep],[M16,M16],[T54,T54],[T80,T80]
            ]:
            wins = {"pars":0}
            number_of_tests_to_run = 10000 # ne pas toucher !
            for x in range(1,number_of_tests_to_run):
                unit1 = GroundUnit(u1)
                unit1.name = "{}_1".format(unit1.name)
                unit2 = GroundUnit(u2)
                unit2.name = "{}_2".format(unit2.name)
                try:
                    wins[unit1.name]
                except KeyError:
                    wins[unit1.name] = 0
                    wins[unit2.name] = 0
                winner = conflict.resolve(unit1,unit2)
                if winner:
                    wins[winner.name] += 1
                else:
                    wins["pars"] += 1

            print("RESULTS:\n{}: {}\n{}: {}\nPars: {}".format(
                unit1.name, wins[unit1.name],
                unit2.name, wins[unit2.name],
                wins["pars"]
                ))
            factor = 20
            '''
            La différence en terme de nombre de victoires ne peut pas dépasser
            1/20ème du nombre de victoire de l'unité 1 ou 2
            '''
            self.assertTrue(abs(wins[unit1.name]-wins[unit2.name])<min(wins[unit1.name]/factor,wins[unit2.name]/factor))
            print("Max diffs: {} / {}".format(wins[unit1.name]/factor, wins[unit2.name]/factor))

if __name__ == '__main__':
    unittest.main(verbosity=9)
