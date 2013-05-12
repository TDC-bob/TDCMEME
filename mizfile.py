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
            raise Exceptions.Error("Impossible d'accéder au fichier", "Erreur fatale pendant la décompression du fichier suivant: {} (peut-être s'agit-il d'un dossier ?)".format(self.path))
        self.logger.debug("ZIP format is correct")
        self.logger.info("all sanity checks OK")

    @logged
    def decompact(self):
        with zipfile.ZipFile(self.path) as zip_file:
            try:
                zip_content = zip_file.infolist()
                self.files_in_zip = [f.filename for f in zip_content]
                self.logger.debug("contenu du fichier zip: {}".format(", ".join(self.files_in_zip)))
                for item in zip_content:
                    # Je n'utilise pas ZipFile.extractall() parce que ça pourrait potentiellement être une faille de sécurité
                    # (extraction en dehors du répertoire qui m'intéresse)
                    try:
                        self.logger.info("Compress type: {}".format(item.compress_type))
                        zip_file.extract(item, self.temp_dir)
                        self.logger.debug('extraction OK: {}'.format(item.filename))
                    except RuntimeError:
                        raise Exceptions.CouldNotExtract(self.path, item, self.logger)
            except zipfile.BadZipFile:
                raise Exceptions.Error("erreur lors de la décompression du fichier MIZ","Chemin vers le fichier: {}".format(self.path), self.logger)
        self.logger.debug("parsing content ...")
        filelist = os.listdir(self.temp_dir)
        for f in ["mission","options","warehouses"]:
            if not f in filelist:
                raise Exceptions.Error("Fichier manquant", 'Impossible de trouver le fichier {} après extraction ({})'.format(f, self.path))
        self.logger.info("ZIP file content: {}".format(str(filelist)))

    @logged
    def recompact(self):
        self.out_mizFile = os.path.join(self.folder, "".join([self.filename,"_out",self.ext]))
        self.logger.info("Fichier de sortie: {}".format(self.out_mizFile))
        with zipfile.ZipFile(self.out_mizFile, mode='w', compression=8) as zip_file:
            for f in self.files_in_zip:
                full_path_to_file = os.path.join(self.temp_dir,f)
                zip_file.write(full_path_to_file,arcname=f)

    def delete_temp_dir(self):
        try:
            shutil.rmtree(self.temp_dir)
        except:
            raise Exceptions.Error("Impossiblede supprimer le répertoire temporaire","Impossible de supprimer le répertoire temporraire suivant: {}".format(self.temp_dir))



