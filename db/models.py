#!/usr/bin/python3
# -*- coding: utf-8 -*-

from django.db import models
#import Default_Werte as Initial


# Basismodell abstract!
class BasisModell(models.Model):
    erstellt = models.DateTimeField(auto_now_add = True)
    zuletzt_geaendert = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


# Abstrake Klases für das Grundschema eines Verfahrens
class Verfahren(BasisModell):



# Klasse für den Ort der Kläranlage
class Ort(models.Model):
    ort = models.CharField(max_length = 100, default = "")


# Klasse für die Datenbankabbildung der Kläranlaged
class Klaeranlage(BasisModell):
    name = models.CharField(max_length = 100)
    ort_ID = models.ForeignKey(Ort, default = 0)
    zuletzt_aktiv = models.BooleanField(default = False)
    abwasserabgabe_phosphor = models.DecimalField(max_digits = 10, decimal_places = 9, default = 2.0)
    kosten_schlammentsorgung = models.DecimalField(max_digits = 10, decimal_places = 9, default = 0.0)
    #wert1 = models.CharField(max_length = 50, default = Initial.wert_1)
    #wert2 = models.CharField(max_length = 50, default = "nope")


class Probenahmestelle(BasisModell):
    abkuerzung = models.CharField(max_length = 10, default = "")
    stelle = models.CharField(max_length = 50, default = "")
    hilfetext = models.TextField(max_length = 200, default = "")


# Probe Zeitspanne
class Probe_Zeitspanne(BasisModell):
    zeitraum = models.CharField(max_length = 20, default = "")


# Probe flüssig
class Probe(BasisModell):
    klaeranlage_ID = models.ForeignKey(Klaeranlage)
    probe_zeitspanne_ID = models.ForeignKey(Probe_Zeitspanne)
    durchfluss = models.DecimalField(max_digits = 10, decimal_places = 9, default = 0.0)
    p_ges = models.DecimalField(max_digits = 10, decimal_places = 9, default = 0.0)
    n_ges = models.DecimalField(max_digits = 10, decimal_places = 9, default = 0.0)
    gerechnet = models.NullBooleanField(default = None)


# Probe Asche/Schlamm
class Probe_Asche(BasisModell):
    klaeranlage_ID = models.ForeignKey(Klaeranlage)
    probe_zeitspanne_ID = models.ForeignKey(Probe_Zeitspanne)
    menge = models.DecimalField(max_digits = 10, decimal_places = 9, default = 0.0)
    entsorgungskosten = models.DecimalField(max_digits = 10, decimal_places = 9, default = 0.0)


# Verfahren
class Verfahren(BasisModell):
    klaeranlage_ID = models.ForeignKey(Klaeranlage)
    ansatzpunkt = models.ForeignKey(Probenahmestelle)
    prozent_entnahme = models.DecimalField(max_digits = 10, decimal_places = 9)
    investkosten = models.DecimalField(max_digits = 10, decimal_places = 9)
    betriebskosten = models.DecimalField(max_digits = 10, decimal_places = 9) # Pro kg P
    verkaufserloes = models.DecimalField(max_digits = 10, decimal_places = 9) # Pro kg P

    class Meta:
        abstract = True

    # Funktion zum exportieren im CSV-Format
    def CSV_export(self, titelzeile = False):
        pass

    #Funtion zum importieren im CSV-Format
    def CSV_import(self, titelzeile = False):
        pass

    def ausgabe(self):
        print(self.id)

    def treeview_ausgabe(self):
        return str(self.id) +" "+ self.name +" "+ self.ort +" "+ self.wert1 +" "+ self.wert2