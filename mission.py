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


from _logging._logging import logged, mkLogger
import _slpp, logging, Exceptions, mizfile, os.path
mkLogger(__name__,logging.INFO)

class Mission():
    """
    Context-manager pour la classe __ManagedMission

    Le contexte permet de s'assurer que toutes les opérations satellites sont
    effectuées avant et après l'instanciationde l'object "Mission"
    """
    def __init__(self, path_to_miz_file, temp_dir=None):
        self.path_to_miz_file = path_to_miz_file
        self.temp_dir = temp_dir

    def __enter__(self):
        self.mission_object = _ManagedMission(self.path_to_miz_file,self.temp_dir)
        return self.mission_object

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            pass
        self.mission_object.finalize()
        self.mission_object.close()

class _ManagedMission():
    """
    NE PAS INSTANCIER

    Cette classe représente (à bas niveau) un fichier mission, lui-même contenu
    dans un fichier *.miz

    L'abstraction permet de gérer la "table de mission", tableau lua constituant
    la mission en elle-même. Tous les autres fichiers contenus dans le *.miz
    (graphiques pour le briefing, fichiers sons, fichiers "options", ...) ne sont
    pas traités ici; pour vérifier la concordance entre le tableau et le contenu
    réel du fichier *.miz, on fera appel à l'attribut "self.miz_file.zip_content"
    """

    @logged
    def __init__(self, path_to_miz_file, temp_dir=None):
        self.logger.info("instanciation d'un nouvel object mission: {}".format(path_to_miz_file))
        self.mizfile = mizfile.MizFile(path_to_miz_file).check().decompact()
        self.logger.debug("miz_file checkée et decompressée dans: {}".format(self.mizfile.temp_dir))
        self.path_to_mission_file = os.path.join(self.mizfile.temp_dir,"mission")
        self.logger.debug("chemin complet vers le fichier mission: {}".format(self.path_to_mission_file))
        parser = _slpp.SLPP()
        try:
            with open(self.path_to_mission_file,mode="r",encoding="UTF-8") as file:
                self.logger.debug("lecture du contenu du fichier mission")
                self.raw_text = file.read()
        except:
            Exceptions.Error("Erreur fatale lors de la lecture du fichier mission",
                            "Impossible de lire le fichier mission suivant: {}".format(self.path_to_mission_file))
        self.logger.debug("délégation de la table de mission au parser SLPP")
        self.d = parser.decode(self.raw_text)
        self.check()

    def finalize(self):
        pass

    def close(self):
        self.mizfile.delete_temp_dir()

    def __level1(self):
        return ('"usedModules"','"groundControl"','"descriptionBlueTask"',
                '"start_time"','"pictureFileNameB"','"currentKey"','"trigrules"',
                '"sortie"','"coalitions"','"descriptionText"','"resourceCounter"',
                '"theatre"','"needModules"','"map"','"forcedOptions"','"failures"',
                '"result"','"triggers"','"goals"','"version"','"pictureFileNameR"',
                '"descriptionRedTask"','"weather"','"coalition"','"trig"')

    @logged
    def check(self):
        """
        Compare la table de mission à une liste prédeterminée, pour vérifier la
        présence de toutesles informations nécessaires
        """
        self.logger.info("vérification de la cohérence de la table")
        self.__check_dict(self.d, self.__level1())

    def __check_dict(self,d,proof):
        """
        Vérifies que le dictionnaire "d" possède toutes les clefs reprises dans "proof"
        """
        d_keys = d.keys()
        try:
            for p in proof:
                sub_dict = d[p]
                if not p in d_keys:
                    raise KeyError
    ##            print(p)
        except KeyError:
            raise Exceptions.Error("Erreur lors de la vérification du fichier mission",
            "impossible de trouver la clef \"{}\" dans la table de mission: {}"
            .format(p, os.path.dirname(self.path_to_mission_file)), self.logger)

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

