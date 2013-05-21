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

from Exceptions import Error
from _logging._logging import logged, mkLogger, DEBUG, INFO
logger = mkLogger(__name__, DEBUG)

weights = ["light","medium","heavy"]
roles = ["assault","support","recce","artyt","c2c","ecm","ew","logistics"]
types = ["vehicle","infantry","deployed","structure"]

class GroundUnit():
    '''
    Représente une classe-démo pour une unité au sol

    Cette classe est appelée à devenir la meta-classe parente pour toutes
    les unités au sol. Les valeurs par défaut y seront définies, ainsi que
    les méthodes communes, telles que "move", "engage", "flee", "entranch",
    "resupply", "surrender". Les sous méthodes (moral, composition, évaluation
    des chances avant combat, etc ...) seront gérées par des méthodes issues
    des classes de gestion du théâtre
    '''
    @logged
    def __init__(self,args):
        '''
        Below are default & average value for a ground unit
        '''
        if not type(args) == dict:
            raise Error("paramètre incorrect", "je m'attendais à recevoir un dictionnaire, et j'ai eu ceci: {}".format(type(args)),self.logger)
        param_list = ["name","role","weight","unit_type","against","division",
                        "speed_on_map","speed_on_ground","unit_range","fuel",
                        "ammo","aggro","group_count","group_size","cost_to_buy",
                        "max_size","moral"]
        err = "paramètre manquant lors de l'instanciation d'une unité au sol"
        for param in param_list:
            try:
                self.__dict__[param] = args[param]
            except KeyError:
                raise Error(err, "il manque le paramètre suivant: {}".format(param),self.logger)
        return
        if args.name == None:
            raise Error(err, "il manque le nom de l'unité", self.logger)
        print(args.name)
        return self
        # all that is below is only a place holder for the IDE to know
        # what I want to export, and to describe the STUB of a ground unit
        # to everybody else
        self.name = "T54" # petty name for the unit
        self.role = "Assault" # could be recce, assault, arty, C2C, ECM, EW, logistic, ...
        self.weight = "Medium" # count as main comparator for force compare.
        self.unit_type = "Vehicle" # can be Vehicle, Infantry, Deployed (arty), Structure, ...
        self.against = {
            light: 80,
            medium: 60,
            heavy: 40
        }
        '''
        Le "poids" (weight) de l'unité joue dans les calculs "pierre-papiers-ciseaux".
        Un groupe de chars T54 ne fera qu'une bouchée d'un groupe de Jeeps Recce (léger),
        parce que le T54 a un rapport de 60 contre les unités légères, et que les Jeeps Recce
        ont un rapport quasiment nul contre le T54.

        Par contre, un groupe de fantassin-bazooka (léger), aura un excellent rapport contre tout
        ce qui est véhicule, particulièrement légers et lents, un peu moins s'ils sont lourds ou
        rapides. Donc, un affrontement entre une section d'infanterie d'assaut anti char (fantassin, unité
        légère) et un groupe de chars T80 (unité lourde, mais lente et balèze) ne tournera pas *forcément*
        en faveur de l'un ou de l'autre.

        Les deux facteurs a prendre en compte lors d'un affrontement "équilibré" (entendre: un affrontement
        où aucune des deux parties ne cherche à fuir) sont le MORAL et la CHANCE. La chance est
        simplement un "jet de dés", modifié par le rapport de force entre les unités (nombre, puissance).

        Le moral, par contre, est tout d'abord défini par une valeur de base, qui est modifiée entre
        les missions en fonction du résultat global du camp de l'unité. Ensuite, une kyrielle d'autres
        modificateurs s'appliquent, parmi lesquels (de tête):
            - distance de l'unité amie la plus proche
            - quantité d'unité amies sur les cases adjacentes
            - l'unité reçoit ou pas un soutien aérien/artillerie ce tour
            - temps depuis le dernier combat, et issue du dernier combat
            - l'unité subit le soutien aérien/arty de l'ennemi
            - l'unité se fait (ou pas) insulter en verlan par Fenlabise
            - etc, etc ...
        '''
        self.division = None # parent division of the unit
        self.speed_on_map = 1 # can move 1 square per "turn" (pure recce units up to 2, maybe ?)
        self.speed_on_ground = 4 # ranging from 1 to 10, maybe
        self.unit_range = 0 # cannot fire to adjacent squares (arty would be "1", super-arty/MLRS up to "2")
        self.fuel = 4 # can move four squares before needing re-supplies
        self.ammo = 4 # can engage four times before running out of ammo
        self.moral = 10 # average starting value for every unit
        self.aggro = 2 # unit will try to make contact with reasonable odds
                        # 0: unit will do whatever it takes to avoid the enemy
                        # 1: unit will try to outmanoeuver the enemy, and will flee superior or matching forces
                        # 3: unit will actively seek enemy contact, even when their
                        #   chances are quite low (it won't commit suicide, but it
                        #   sure will stand its ground)
        self.group_count = 4 # unit is made out of 4 groups
        self.group_size = 8 # each group is made out of 8 individual units
        self.cost_to_buy = 50 # the amount of economical resources to buy ONE GROUP
        self.max_size = 5 # the maximum amount of groups in this unit
        '''
        Pour clarifier les 4 derniers points (group_count, group_size, cost_to_buy et max_size),
        un groupe de T54 de base compte en tout 32 chars, répartis en 4 groupes de 8.
        Si l'ennemi souhaite remplacer ou renforcer son unité, il devra dépenser 50
        ressources économique, et recevra en échange un nouveau groupe de 8 chars.
        Cependant, il ne pourra pas renforcer son unité au délà de 5 groupes, pour
        un maximum de 40 chars en tout
        '''

    def __str__(self):
        return '''
    Name: {}
    '''.format(self.name)

    def flee(self, opponent):
        if self.ammo == 0:
            return True
        odds = self.aggro
##        if self.against[opponent.weight] > 80:
##            odds += 2
##        elif self.against[opponent.weight] > 50:
##            odds += 1
##        elif self.against[opponent.weight] < 20:
##            odds -= 1
        odds = odds * (self.against[opponent.weight]/10)
        odds = odds * (self.moral /10)
        print("Odds for {}: {}".format(self.name, odds))


'''
self.name = "T54" # petty name for the unit
self.role = "Assault" # could be recce, assault, arty, C2C, ECM, EW, logistic, ...
self.weight = "Medium" # count as main comparator for force compare.
self.unit_type = "Vehicle" # can be Vehicle, Infantry, Deployed (arty), Structure, ...
self.against = {
    light: 80,
    medium: 60,
    heavy: 40
}
self.speed_on_map = 1 # can move 1 square per "turn" (pure recce units up to 2, maybe ?)
self.speed_on_ground = 4 # ranging from 1 to 10, maybe
self.unit_range = 0 # cannot fire to adjacent squares (arty would be "1", super-arty/MLRS up to "2")
self.fuel = 4 # can move four squares before needing re-supplies
self.ammo = 4 # can engage four times before running out of ammo
self.moral = 10 # average starting value for every unit
self.aggro = 2 # unit will try to make contact with reasonable odds
self.group_count = 4 # unit is made out of 4 groups
self.group_size = 8 # each group is made out of 8 individual units
self.cost_to_buy = 50 # the amount of economical resources to buy ONE GROUP
self.max_size = 40 # the maximum amount of units whatsoever
'''

def main():
    pass

if __name__ == '__main__':
    main()