# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     10/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# coding=utf-8


import logging, makeTemp
from _logging import mkLogger, logged
logger = mkLogger(__name__, logging.DEBUG )

##from os.path import isfile, exists, join, abspath, dirname, basename
import os, shutil, zipfile, Exceptions
##from os import remove, mkdir, rename, listdir
##from shutil import copyfile, rmtree
##from os.path import exists, basename, dirname
##import string, zipfile, Exceptions

class MizFile:
    @logged
    def __init__(self, path_to_file, temp_dir=None):
        self.logger.info("Initializing MizFile({},{})".format(path_to_file,temp_dir))
        self.path = path_to_file
        self.basename = os.path.basename(path_to_file)
        split = os.path.splitext(self.basename)
        self.filename = split[0]
        self.ext = split[1]

        if self.ext != ".miz":
            self.logger.warning("extention for this file is \"{}\", where \".miz\" was expected")

        self.logger.debug("Basename: {}".format(self.basename))
        self.folder = os.path.dirname(path_to_file)
        self.logger.debug("Path to file: {}".format(self.folder))

        if temp_dir == None:
            self.temp_dir = makeTemp.random_folder(self.folder, prefix="".join([self.filename,"_"]))
        else:
            self.temp_dir = temp_dir
        self.logger.debug("temporary directory for this MIZ will be: {}".format(self.temp_dir))

    @logged
    def check(self):
        self.logger.info("runing sanity checks")
        self.logger.debug("checking for existence ...")
        if not os.path.exists(self.path):
            raise Exceptions.FileDoesNotExist(self.path,self.logger)
        self.logger.debug("files exists")
        self.logger.debug("checking for ZIP consistency ...")
        try:
            with zipfile.ZipFile(self.path) as zip_file:
                corruptedFile = zip_file.testzip()
                if corruptedFile:
                    raise zipfile.BadZipFile
        except zipfile.BadZipFile:
            raise Exceptions.InvalidMizFile(self.path, self.logger, "le fichier MIZ est corrompu")
        except PermissionError:
            raise Exceptions.Error("Could not access file", "Fatal error while trying to unzip following file: {} (could be it's a folder, or it's read-protected)".format(self.path))
        self.logger.debug("ZIP format is correct")
        self.logger.info("all sanity checks OK")

    @logged
    def decompact(self):
        with zipfile.ZipFile(self.path) as zip_file:
            try:
                zip_content = zip_file.infolist()
                self.logger.debug("contenu du fichier zip: {}".format(", ".join([f.filename for f in zip_content])))
                for item in zip_content:
                    # Je n'utilise pas ZipFile.extractall() parce que ça pourrait potentiellement être une faille de sécurité
                    # (extraction en dehors du répertoire qui m'intéresse)
                    try:
                        zip_file.extract(item, self.temp_dir)
                        self.logger.debug('extraction OK: {}'.format(item.filename))
                    except RuntimeError:
                        raise Exceptions.CouldNotExtract(self.path, item, self.logger)
            except zipfile.BadZipFile:
                raise Exceptions.Error("erreur lors de la décompression du fichier MIZ","Chemin vers le fichier: {}".format(self.path), self.logger)
            self.__parse_content()

    def __parse_content(self):
        self.logger.debug("parsing content ...")
        filelist = os.listdir(self.temp_dir)
        if not "mission" in filelist:
            raise Exceptions.Error("Fichier manquant", 'Impossible de trouver le fichier "mission" après extraction ({})'.format(self.path))
        if not "options" in filelist:
            raise Exceptions.Error("Fichier manquant", 'Impossible de trouver le fichier "options" après extraction ({})'.format(self.path))
        if not "warehouses" in filelist:
            raise Exceptions.Error("Fichier manquant", 'Impossible de trouver le fichier "warehouses" après extraction ({})'.format(self.path))
        self.logger.info("ZIP file content: {}".format(str(filelist)))
        self.zip_content = filelist


##    def __temp(self):
##        try:
##            with ZipFile(self.path) as file:
##                corruptedFile = file.testzip()
##                if corruptedFile:
##                    raise Exceptions.InvalidMizFile(self.path, self.logger, "fichier miz corrompu, impossible de l'ouvrir en tant que fichier zip")
####                self.logger.debug("rÃ©cupÃ©ration de l'objet infolist() Ã  partir de l'objet zipfile()")
##                infoList = file.infolist()
##                for item in infoList:
##                    # Je n'utilise pas ZipFile.extractall() parce que Ã§a pourrait potentiellement Ãªtre une faille de sÃ©curitÃ©
##                    # (extraction en dehors du rÃ©pertoire qui m'intÃ©resse)
##                    try:
##                        file.extract(item, tempDir)
##                        ##self.logger.debug('extraction de "{}" rÃ©ussie'.format(item.filename))
##                    except RuntimeError:
##                        raise Exceptions.CouldNotExtract(self.path, item, self.logger)
##                ##self.logger.debug("objet infolist rÃ©cupÃ©rÃ©, vÃ©rification du contenu du fichier MIZ")
##                # Fichier mission
##                self.mission = abspath(join(tempDir, "mission"))
##                if not exists(self.mission):
##                    raise Exceptions.MissingObjectInZipFile(self.path, "mission", self.logger)
##                self.options = abspath(join(tempDir, "options"))
##                if not exists(self.options):
##                    raise Exceptions.MissingObjectInZipFile(self.path, "options", self.logger)
##                self.warehouses = abspath(join(tempDir, "warehouses"))
##                if not exists(self.warehouses):
##                    self.logger.warning("ce fichier MIZ ne contient pas de fichier warehouses")
##        except BadZipFile:
##            raise Exceptions.InvalidMizFile(self.path, self.logger, "le fichier MIZ est corrompu")