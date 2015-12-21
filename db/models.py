#!/usr/bin/python3
# -*- coding: utf-8 -*-

from django.db import models

# Basismodell abstract!
class BasisModell(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    touched = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

# Klasse für die Datenbankabbildung der Kläranlage
class Klaeranlage(BasisModell):
    name = models.CharField(max_length = 100)
    ort = models.CharField(max_length = 50)
    wert1 = models.CharField(max_length = 50, default = "nope")
    wert2 = models.CharField(max_length = 50, default = "nope")

    # Funktion zum exportieren im CSV-Format
    def CSV_export(self, titelzeile = False):
        pass

    #Funtion zum importieren im CSV-Format
    def CSV_import(self, titelzeile = False):
        pass

