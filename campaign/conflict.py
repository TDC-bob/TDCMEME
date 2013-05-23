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

from random import randint
from copy import deepcopy

from _logging._logging import mkLogger, logged, DEBUG, INFO
logger = mkLogger(__name__)

class Conflict():
    @logged
    def __init__(self, attacker, defender):
        self.logger.debug("Instanciating a new conflict between {} (attacking) and {} (defending)"
            .format(attacker.name, defender.name))
##        self.a = deepcopy(attacker)
##        self.d = deepcopy(defender)
        self.round_count = 0
        self.resolved = False
        self.outcome = ""
        self.a = attacker
        self.d = defender
        self.a.has_fled = False
        self.d.has_fled = False
        self.a_has_fled = self.d_has_fled = False
##        if self.d.is_entranched: # give a boost to the defender if he's entranched
##            self.d_random += randint(20,40)

    def resolve(self):
        self.logger.debug("resolving conflict between {} and {}".format(self.a.name, self.d.name))
        self._resolve_round()
        self.winner = []
        self.destroyed= []
        self.fled = []
        if not self.a.is_alive:
            self.outcome = "{} has been destroyed, {} wins".format(self.a.name, self.d.name)
            self.destroyed.append(self.a)
        if not self.d.is_alive:
            self.outcome = "{} has been destroyed, {} wins".format(self.d.name, self.a.name)
            self.destroyed.append(self.d)
        if self.a.has_fled and self.d.has_fled:
            self.outcome = "both unit fled"
            self.fled.append(self.a)
            self.fled.append(self.d)
        elif self.a.has_fled:
            self.outcome = "{} has fled, {} wins".format(self.a.name, self.d.name)
            self.fled.append(self.a)
        elif self.d.has_fled:
            self.outcome = "{} has fled, {} wins".format(self.d.name, self.a.name)
            self.fled.append(self.d)
        if (self.a.has_fled or not self.a.is_alive) and (self.d.is_alive and not self.d.has_fled):
            self.winner.append(self.d)
        elif (self.d.has_fled or not self.d.is_alive) and (self.a.is_alive and not self.a.has_fled):
            self.winner.append(self.a)
        self.logger.debug("{} after {} rounds".format(self.outcome, self.round_count))
        return self.winner, self.fled, self.destroyed

    def _resolve_round(self):
        '''
        aggro: base value
        moral: base multiplicator
        against + opponent
        speed_on_ground + opponent
        current_size() + opponent
        '''
        self.round_count += 1
        rtn = False
        self._should_flee()
        if self.a_should_flee:
            self._flee(self.a, self.d)
            rtn = True
        if self.d_should_flee:
            self._flee(self.d, self.a)
            rtn = True
        self._apply_damage()
        if self.a.size < 1:
            self.a.is_alive = False
            rtn = True
        if self.d.size < 1:
            self.d.is_alive = False
            rtn = True
        if rtn:
            return
        self._resolve_round()


    def _apply_damage(self):
        self.logger.debug("applying damages")
        a_size = self.a.current_size()
        d_size = self.d.current_size()
        self.a_random = randint(0,15)
        self.d_random = randint(0,15)
        if not self.a_has_fled:
            self.logger.debug("size mod: {}".format((100-self.d.against[self.a.weight]*d_size+self.d_random)/100))
            self.a.size *= (100-self.d.against[self.a.weight]*d_size+self.d_random)/100
            self.logger.debug("{} new size: {}".format(self.a.name, self.a.size))
        if not self.d_has_fled:
            self.logger.debug("size mod: {}".format((100-self.a.against[self.d.weight]*a_size+self.a_random)/100))
            self.d.size *= (100-self.a.against[self.d.weight]*a_size+self.a_random)/100
            self.logger.debug("{} new size: {}".format(self.d.name, self.d.size))
        if self.a.size < 1:
            self.a.is_alive = False
        if self.d.size < 1:
            self.d.is_alive = False

    def _calculate_odds(self, unit, opponent):
        odds = unit.moral/10
        self.logger.debug("odds moral: {}".format(odds))
        mult = 1
        size_ratio = unit.current_size() / opponent.current_size()
        self.logger.debug("size_ratio: {}".format(size_ratio))
        mult *= size_ratio + unit.aggro*0.75

        own_power = unit.against[opponent.weight]*unit.current_size()
        opponent_power = opponent.against[unit.weight]*opponent.current_size()
        power_mult = (own_power / opponent_power) if (opponent_power > 0) else 10
        mult *= power_mult
        self.logger.debug("power_mult: {}".format(power_mult))

        speed_mult = (unit.speed_on_ground / opponent.speed_on_ground)
        if speed_mult > 1:
            speed_mult -= (speed_mult - 1) / 2
        else:
            speed_mult += (1-speed_mult) / 2
        self.logger.debug("speed_mult: {}".format(speed_mult))
        mult *= speed_mult
        self.logger.debug("mult speed: {}".format(mult))

        odds *= mult
        self.logger.debug("{} odds: {}".format(unit.name, odds))
        return odds


    def _flee(self, unit, opponent):
        self.logger.debug("{} is fleeing".format(unit.name))
        if unit.speed_on_ground < opponent.speed_on_ground and not opponent.has_fled:
            self.logger.debug("{} is taking some damage in the process".format(unit.name))
            self._apply_damage()
        unit.has_fled = True

    def _should_flee(self):
        self.a_should_flee = (10-self.a.aggro)/10 >= self._calculate_odds(self.a, self.d)
        self.d_should_flee = (10-self.d.aggro)/10 >= self._calculate_odds(self.d, self.a)
        self.logger.debug("{} should flee: {}".format(self.a.name,self.a_should_flee))
        self.logger.debug("{} should flee: {}".format(self.d.name,self.d_should_flee))


def main():
    pass

if __name__ == '__main__':
    main()
