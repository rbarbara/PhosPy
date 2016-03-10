#!/usr/bin/python3
# -*- coding: utf-8 -*-

from django.db import models


# Basismodell abstract!
# Damit jeder Datenbankeintrag ein Datum für zuletzt verändert und für erstellt enthält
class BasisModell(models.Model):
    erstellt = models.DateTimeField(auto_now_add = True)
    zuletzt_geaendert = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


# Klasse für den Ort der Kläranlage
class Ort(models.Model):
    ort = models.CharField(max_length = 50, default = "")


# Zeitspanne
class Zeitspanne(BasisModell):
    zeitraum = models.CharField(max_length = 20, default = "")
    zeitraum_pro = models.CharField(max_length = 20, default = "")


# Klasse für die Datenbankabbildung der Kläranlage
class Klaeranlage(BasisModell):
    name = models.CharField(max_length = 100)
    ort = models.ForeignKey(Ort, default = 0)
    zuletzt_aktiv = models.BooleanField(default = False)
    zeitschritt_zuletzt_angezeigt = models.ForeignKey(Zeitspanne, default = 1)
    abwasserabgabe_p = models.DecimalField(max_digits = 10, decimal_places = 5, default = 11.93)
    abwasserabgabe_n = models.DecimalField(max_digits = 10, decimal_places = 5, default = 7.158)
    kosten_schlammentsorgung = models.DecimalField(max_digits = 10, decimal_places = 5, default = 0.0)


# Probenahmestelle
class Probenahmestelle(BasisModell):
    abkuerzung = models.CharField(max_length = 10, default = "")
    stelle = models.CharField(max_length = 50, default = "")
    hilfetext = models.TextField(max_length = 200, default = "")


# Probe flüssig
class Probe_fluessig(BasisModell):
    klaeranlage = models.ForeignKey(Klaeranlage, default = 1)
    #probe_zeitspanne_ID = models.ForeignKey(Zeitspanne, default = 1)
    probe_probenahmestelle = models.ForeignKey(Probenahmestelle, default = 1)
    durchfluss = models.DecimalField(max_digits = 13, decimal_places = 3, default = 0.0)
    p_ges = models.DecimalField(max_digits = 13, decimal_places = 3, default = 0.0)
    p_po4 = models.DecimalField(max_digits = 13, decimal_places = 3, default = 0.0)
    gerechnet = models.NullBooleanField(default = None)


# Probe Asche/Schlamm
class Probe_Schlamm_Asche(BasisModell):
    klaeranlage = models.ForeignKey(Klaeranlage, default = 1)
    #probe_zeitspanne_ID = models.ForeignKey(Zeitspanne, default = 1)
    probe_probenahmestelle = models.ForeignKey(Probenahmestelle, default = 1)
    menge = models.DecimalField(max_digits = 13, decimal_places = 3, default = 0.0)
    p_ges_massengehalt = models.DecimalField(max_digits = 13, decimal_places = 3, default = 0.0)
    gerechnet = models.NullBooleanField(default = None)


# Verfahren, Abstrakte Klasse, nur als Vorlage für verschiedene Verfahren mit dem immer gleichen Grundgerüst!
class Verfahren(BasisModell):
    klaeranlage = models.ForeignKey(Klaeranlage)
    #ansatzpunkt = models.ForeignKey(Probenahmestelle)
    p_prozent_entnahme = models.DecimalField(max_digits = 5, decimal_places = 2)
    investkosten = models.DecimalField(max_digits = 13, decimal_places = 3)
    betriebskosten_pro_p = models.DecimalField(max_digits = 13, decimal_places = 3) # Pro kg P
    verkaufserloes_pro_p = models.DecimalField(max_digits = 13, decimal_places = 3) # Pro kg P
    zeitspanne_abschreibung = models.DecimalField(max_digits = 5, decimal_places = 2)
    #auf_zeitspanne_angewendet = models.ForeignKey(Zeitspanne)

    class Meta:
        abstract = True


# Verfahren welches am Ablauf der Kläranlage ansetzt
class Verfahren_Ablauf(Verfahren):
    pass


# Verfahren welches beim Schlammwasser was zurück in die Biologie geht ansetzt
class Verfahren_Schlammwasser(Verfahren):
    n_nh4_vorher = models.DecimalField(max_digits = 13, decimal_places = 3)
    n_nh4_nachher = models.DecimalField(max_digits = 13, decimal_places = 3)


# Verfahren welches beim Faulschlamm ansetzt
class Verfahren_Faulschlamm(Verfahren):
    kosten_schlammentsorgung = models.DecimalField(max_digits = 13, decimal_places = 3)


# Verfahren welches bei der Asche ansetzt
class Verfahren_Asche(Verfahren):
    kosten_schlammverbrennung = models.DecimalField(max_digits = 13, decimal_places = 3)
