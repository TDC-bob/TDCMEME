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

import ground_unit
import random

example1 = {
    "name":"exemple_1",
    "role":"assault",
    "weight": "heavy",
    "unit_type": "vehicle",
    "against": {"light":75,"medium":60,"heavy":40},
    "division":None,
    "speed_on_map":1,
    "speed_on_ground":5,
    "unit_range": 0,
    "fuel": 4,
    "ammo": 4,
    "moral": 10,
    "aggro": 2,
    "group_count": 4,
    "group_size": 8,
    "cost_to_buy": 50,
    "max_size": 40
    }
example2 = {
    "name":"exemple_2",
    "role":"assault",
    "weight": "medium",
    "unit_type": "vehicle",
    "against": {"light":75,"medium":50,"heavy":25},
    "division":None,
    "speed_on_map":1,
    "speed_on_ground":5,
    "unit_range": 0,
    "fuel": 4,
    "ammo": 4,
    "moral": 10,
    "aggro": 2,
    "group_count": 4,
    "group_size": 8,
    "cost_to_buy": 50,
    "max_size": 40
}

def resolve(unit1, unit2):

    unit1_chances = unit1.against[unit2.weight]
    unit2_chances = unit2.against[unit1.weight]
    unit1.flee(unit2)
    unit2.flee(unit1)
##    print(random.randint(20,80))

def main():
    unit1 = ground_unit.GroundUnit(example1)
    unit2 = ground_unit.GroundUnit(example2)
    resolve(unit1,unit2)

if __name__ == '__main__':
    main()
