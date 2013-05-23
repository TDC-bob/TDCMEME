﻿# -*- coding: UTF-8 -*-
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

from random import randint

def resolve(unit1,unit2):
    '''
    DÃƒÂ©termine le gagnant d'un conflit sur la carte

    Le retour peut-ÃƒÂªtre soit l'unitÃƒÂ© qui a gagnÃƒÂ©, soit "None" dans le cas oÃƒÂ¹ les
    deux unitÃƒÂ©s ont fui le combat (les lÃƒÂ¢ches !)
    '''
    winner = None
    unit1_fled = unit2_fled = False

    unit1_fled = unit1.flee(unit2)
##    print("unit1 fled: {}".format(unit1_fled))
    unit2_fled = unit2.flee(unit1)
##    print("unit2 fled: {}".format(unit2_fled))

    if unit1_fled and unit2_fled:
        return None
    elif unit1_fled:
        return unit2
    elif unit2_fled:
        return unit1
    return _resolve_round(unit1,unit2)

def _resolve_round(unit1,unit2):
    unit1_random = randint(0,30)
    unit2_random = randint(0,30)
    unit1_power_mod = unit1.against[unit2.weight] + unit1_random
    unit2_power_mod = unit2.against[unit1.weight] + unit2_random
##    print("unit1_power_mod: {}".format(unit1_power_mod))
##    print("unit2_power_mod: {}".format(unit2_power_mod))
    unit1.size *= unit2_power_mod/100
    unit2.size *= unit1_power_mod/100
##    print("unit1.size :{}".format(unit1.size))
##    print("unit2.size :{}".format(unit2.size))
##    print(unit2.size)
    return resolve(unit1,unit2)




if __name__ == '__main__':
    main()
