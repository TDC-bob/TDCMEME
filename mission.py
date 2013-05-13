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
import _slpp, logging, Exceptions
mkLogger(__name__,logging.DEBUG)

class Mission():
    """
    Représente un fichier mission

    Le fichier mission est lui-même contenu dans un fichier *.miz, il faut donc
    d'abord instancier puis extraire ce dernier, fonctions accessibles via la
    classe mizfile.MizFile
    """

    @logged
    def __init__(self, path_to_mission_file):
        self.logger.info("instanciation d'un nouvel object mission: {}".format(path_to_mission_file))
        parser = _slpp.SLPP()
        with open(path_to_mission_file,mode="r",encoding="UTF-8") as file:
            self.raw_text = file.read()
        self.d = parser.decode(self.raw_text)
        self.check()

    def __level1(self):
        return ('"usedModules"',)
##"groundControl"
##"descriptionBlueTask"
##"start_time"
##"pictureFileNameB"
##"currentKey"
##"trigrules"
##"sortie"
##"coalitions"
##"descriptionText"
##"resourceCounter"
##"theatre"
##"needModules"
##"map"
##"forcedOptions"
##"failures"
##"result"
##"triggers"
##"goals"
##"version"
##"pictureFileNameR"
##"descriptionRedTask"
##"weather"
##"coalition"
##"trig"
##                ]

    @logged
    def check(self):
        self.logger.info("checking mission table consistency")
        self.__check_dict(self.d, self.__level1())

    def __check_dict(self,d,proof):
        """
        Vérifies que le dictionnaire "d" possède toutes les clefs reprises dans "proof"
        """
        d_keys = d.keys()
        for p in proof:
            if not p in d_keys:
                raise Exceptions.Error("Erreur lors de la vérification du fichier mission",
                "Impossible de trouver la clef \"{}\" dans la table de mission".format(p), self.logger)




    @logged
    def short_summary(self):
        """
        Retourne une string avec un mini-résumé de la table de mission

        Présente sous forme indentée les deux premiers niveaux de la table LUA
        du fichier mission
        """
        self.logger.info("returning basic string info about mission's dictionnary")
        primary_keys = self.d.keys()
        rtn = list()
        for k in primary_keys:
            rtn.append(k)
            if type(self.d[k]) == dict:
                rtn.append("\n".join(["\t\t{}".format(kk) for kk in self.d[k].keys()]))
            else:
                rtn.append("\t\t{}".format(self.d[k]))

        return "\n".join(rtn)

