#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
#import sys

# Django-Datenbank importieren
import db.models as db

# Grafik Toolkit imporotieren
import tkinter as tk
import tkinter.ttk as ttk

# Default-Werte importieren
import Default_Werte as default

# Damit das tut... ohne gehen die Special-Gui-Vars nicht
root = tk.Tk()

# Konvertiert von doulbe/float zu String mit Dezimalkomma
def dez_str(input):
    return str(input).replace('.', ',')

# Konvertiert von String mit Dezimalkomma auf Gleitkommazahl
def str_dez(input):
    return float(input.replace(',','.'))



class KA_Datensatz():
    def __init__(self, id = 1):

        # Alle benötigten Variablen bauen
        self.statuszeile = tk.StringVar()
        self.statuszeile.set("Laden..")

        self.id = 1
        # Datensatz
        self.ds = db.Klaeranlage.objects.filter(id = self.id).select_related('ort', 'probe_fluessig', 'probe_schlamm_asche',
            'probenahmestelle', 'verfahren_ablauf', 'verfahren_asche', 'verfahren_faulschlamm',
            'verfahren_schlammwasser', 'zeitspanne')[0]

        self.name = tk.StringVar()
        self.name.set("Default")
        self.ort = tk.StringVar()
        self.ort.set("Default-Wort")


        self.abwasserabgabe_p = tk.DoubleVar()
        self.abwasserabgabe_p.set(default.ABWASSERABGABE_P)
        self.abwasserabgabe_n = tk.DoubleVar()
        self.abwasserabgabe_n.set(default.ABWASSERABGABE_N)
        self.kosten_schlammentsorgung = tk.DoubleVar()
        self.kosten_schlammentsorgung = tk.DoubleVar(default.KOSTEN_SCHLAMMENTSORGUNG)

        # Dictionary für alle Probenahmestellen bauen pro Wert
        self.pns = {}

        # Alle flüssigen Probenahmestellen erstellen und auf Null stellen
        for alle in [1, 2, 3, 4, 5, 6]:
            self.pns[alle] = {}
            self.pns[alle]["p_ges"] = tk.DoubleVar()
            self.pns[alle]["p_ges"].set(0)
            self.pns[alle]["p_po4"] = tk.DoubleVar()
            self.pns[alle]["p_po4"].set(0)
            self.pns[alle]["durchfluss"] = tk.DoubleVar()
            self.pns[alle]["durchfluss"].set(0)

        # Alle nicht-flüssigen Probenahmestellen erstellen und auf Null stellen
        for alle in [7,8]:
            self.pns[alle] = {}
            self.pns[alle]["menge"] = tk.DoubleVar()
            self.pns[alle]["menge"].set(0)
            self.pns[alle]["p_ges_massengehalt"] = tk.DoubleVar()
            self.pns[alle]["p_ges_massengehalt"].set(0)

        # Variablen für die Verfahren bauen erst die die bei allen gleich sind
        self.verf_ablauf = {}
        self.verf_schlammwasser = {}
        self.verf_faulschlamm = {}
        self.verf_asche = {}
        for x in ["p_prozent_entnahme", "investkosten", "betriebskosten_pro_p", "verkaufserloes_pro_p", "zeitspanne_abschreibung"]:
            self.verf_ablauf[x] = tk.DoubleVar()
            self.verf_ablauf[x].set(0)
            self.verf_schlammwasser[x] = tk.DoubleVar()
            self.verf_schlammwasser[x].set(0)
            self.verf_faulschlamm[x] = tk.DoubleVar()
            self.verf_faulschlamm[x].set(0)
            self.verf_asche[x] = tk.DoubleVar()
            self.verf_asche[x].set(0)

        # Zusätzliche Variablen die nicht in jedem Verfahren vorkommen
        self.verf_schlammwasser["n_nh4_vorher"] = tk.DoubleVar()
        self.verf_schlammwasser["n_nh4_vorher"].set(0)
        self.verf_schlammwasser["n_nh4_prozent_entnahme"] = tk.DoubleVar()
        self.verf_schlammwasser["n_nh4_prozent_entnahme"].set(0)
        self.verf_schlammwasser["kosten_schlammentsorgung"] = tk.DoubleVar()
        self.verf_schlammwasser["kosten_schlammentsorgung"].set(0)

        self.verf_faulschlamm["kosten_schlammverbrennung"] = tk.DoubleVar()
        self.verf_faulschlamm["kosten_schlammverbrennung"].set(0)
        self.verf_faulschlamm["n_nh4_vorher"] = tk.DoubleVar()
        self.verf_faulschlamm["n_nh4_vorher"].set(0)
        self.verf_faulschlamm["n_nh4_prozent_entnahme"] = tk.DoubleVar()
        self.verf_faulschlamm["n_nh4_prozent_entnahme"].set(0)

        self.verf_asche["kosten_schlammverbrennung"] = tk.DoubleVar()
        self.verf_asche["kosten_schlammverbrennung"].set(0)

        self.statuszeile.set("Initialisieren fertig")
        print(self.statuszeile.get())


        # Daten_berechnen

    # Fkt lädt einen bestimmten Datensatz
    def lade_datensatz(self, ka_id = 1):
        pass
        # Am Ende Statuszeile auf "Datensatz Nr. bla geladen"
        # Testen ob es den Datensatz überhaupt gibt:
        try:
            self.ds = db.Klaeranlage.objects.get(id = ka_id).select_related('ort', 'probe_fluessig', 'probe_schlamm_asche',
                'probenahmestelle', 'verfahren_ablauf', 'verfahren_asche', 'verfahren_faulschlamm',
                'verfahren_schlammwasser', 'zeitspanne')
            self.id = ka_id
            # Erst den KA Datensatz auslesen
            if not self.lade_klaeranlage():
                return False
            # Dann die Probenahmestellen Datensätze auslesen - alle
            if not self.lade_alle_proben():
                return False
            # Dann die Verfahren Datensätze auslesen
            if not self.lade_alle_verfahren():
                return False

            self.statuszeile.set("Datensatz %s geladen" % str(self.ds.id))
            return True
        except:
            self.statuszeile.set("Den angeforderten Datensatz gibt es nicht oder irgend etwas ist schief gelaufen")
            return False


    # Fkt lädt letzten aktiven Datensatz, das Flag "zuletzt_aktiv" wird dafür ausgelesen
    def lade_letzten_aktiven_datensatz(self):
        try:
            # Alle Datensätze mit dem aktive-Flag heraus holen
            aktive_ds = db.Klaeranlage.objects.filter(zuletzt_aktiv = True)
            # Falls es keinen Datensatz mit dem zuletzt_aktiv Flag gibt, den aktuellen als solchen markieren
            if aktive_ds.count() == 0:
                self.ds.zuletzt_aktiv = True
                self.ds.save()
                return self.lade_datensatz(ka_id = self.ds.id)
            # Falls es mehrere Datensätze mit dem "zuletzt_aktiv" Flag gibt den ersten nehmen und die anderen zurück setzen
            if aktive_ds.count() != 1:
                aktive_ds.update(zuletzt_aktiv = False)
                aktive_ds[0].zuletzt_aktiv = True
                aktive_ds.save()
                # Datensatz ID an die laden-Fkt übergeben
                return self.lade_datensatz(ka_id = aktive_ds[0].id)
        except:
            return False

    # Funktion speichert den aktiven Datensatz als neuen Datensatz oder überschreibt einen alten je nach dem Flag "ueberschreiben"
    # id_ueberschreiben wird ignoriert wenn ueberschreiben = False
    def speicher_datensatz(self, ueberschreiben = False):
        # Genannten Datensatz ueberschreiben
        if ueberschreiben:
            try:
                # Checken ob die ID überhaupt existiert
                self.ds = db.Klaeranlage.objects.get(id = self.id).select_related('ort', 'probe_fluessig',
                    'probe_schlamm_asche', 'probenahmestelle', 'verfahren_ablauf', 'verfahren_asche',
                    'verfahren_faulschlamm', 'verfahren_schlammwasser', 'zeitspanne')
            except:
                status_string = "Datensatz mit der id: " + str(self.id) + " existiert nicht, überschreiben nicht möglich"
                self.statuszeile.set(status_string)
                return False

        # Neuen Datensatz bauen und in self.ds laden
        else:
            # Funktion erstellt kompletten neuen Datensatz und gibt die ID zurück
            self.__new__()
            # Den neu erstellten Datensatz in der DB mit self.ds verknüpfen
            try:
                self.ds = db.Klaeranlage.objects.get(id = self.id).select_related('ort', 'probe_fluessig',
                    'probe_schlamm_asche', 'probenahmestelle', 'verfahren_ablauf', 'verfahren_asche',
                    'verfahren_faulschlamm', 'verfahren_schlammwasser', 'zeitspanne')
            except:
                return False

        # Alles speichern
        try:
            self.speicher_alle_verfahren()
            self.speicher_alle_probenahmestellen()
            self.speicher_klaeranlage()
            self.statuszeile.set("Datensatz #%s geschrieben" % self.id)
            return True
        except:
            return False


    # Funktion erstellt einen neuen leeren Datensatz und gibt die ID des Kläranlagen-Objekts zurück
    def __new__(self):
        try:
            # Ort Objekt neu erstellen und übergeben
            mein_ort = db.Ort.objects.create(ort = "Default Ort")
            mein_ort.save()
            # Kläranlage Objekt erstellen und mit Ort verknüpfen
            meine_ka = db.Klaeranlage.objects.create(ort = mein_ort)
            meine_ka.save()
            # ID aus dem Kläranlagenobjekt holen und merken
            meine_id = meine_ka.id
            # Verfahren Ablauf erstellen und verknüpfen
            mein_verf_abl = db.verfahren_ablauf.objects.create(klaeranlage = meine_ka, ansatzpunkt_id = 3)
            mein_verf_abl.save()
            # Verfahren Schlwammwasser erstellen und verknüpfen
            mein_verf_schlw = db.verfahren_schlammwasser.objects.create(klaeranlage = meine_ka, ansatzpunkt_id = 2)
            mein_verf_schlw.save()
            # Verfahren Faulschlamm erstellen und verknüpfen
            mein_verf_faulschl = db.verfahren_faulschlamm.objects.create(klaeranlage = meine_ka, ansatzpunkt_id = 6)
            mein_verf_faulschl.save()
            # Verfahren Asche erstellen und verknüpfen
            mein_verf_asche = db.verfahren_asche.objects.create(klaeranlage = meine_ka, ansatzpunkt_id = 8)
            mein_verf_asche.save()
            # Probenahmestellen flüssig erstellen und verknüpfen
            for i in [1, 2, 3, 4, 5, 6]:
                meine_probenahmestelle = db.probe_fluessig.objects.create(klaeranlage = meine_ka, probe_probenahmestelle_id = i)
                meine_probenahmestelle.save()
            # Probenahmestellen Schlamm / Asche erstellen und verknüpfen
            for i in [7, 8]:
                meine_probenahmestelle = db.probe_schlamm_asche.objects.create(klaeranlage = meine_ka, probe_probenahmestelle = i)
                meine_probenahmestelle.save()
            self.id = meine_id
            return meine_id
        except:
            return False

    # Einmal alles berechnen neu Triggern
    def alles_berechnen(self):
        # Tu Dinge
        pass

    # Funktion schreibt Kläranlagen Datensatz in die DB
    # self.ds muss vorher schon auf den richtigen DS gesetzt sein!
    def speicher_klaeranlage(self):
        try:
            self.ds.abwasserabgabe_n = self.abwasserabgabe_n.get()
            self.ds.abwasserabgabe_p = self.abwasserabgabe_p.get()
            self.ds.kosten_schlammentsorgung = self.kosten_schlammentsorgung.get()
            # Ort erstellen oder aus der DB holen
            mein_ort = db.Ort.objects.get_or_create(ort = self.org.get())[0]
            mein_ort.save()
            self.ds.ort = mein_ort
            # Kläranlagen Datensatz speichern
            self.ds.save()
            return True
        except:
            return False

    # Fkt schreibt Probenahmestelle in DB
    # self.ds muss vorher schon auf den richtigen DS gesetzt sein!
    def speicher_probenahmestelle(self, pns = 0):
        if pns <= 0:
            return False
        elif pns <= 6:
            try:
                # Passende Probenahmestelle zur KA und zur Stelle aus der DB holen oder erstellen
                meine_probenahmestelle = db.probe_fluessig.objects.get_or_create(klaeranlage = self.ds, probe_probenahmestelle_id = pns)[0]
                meine_probenahmestelle.durchfluss = self.pns[pns]["durchfluss"].get()
                meine_probenahmestelle.p_ges = self.pns[pns]["p_po4"].get()
                meine_probenahmestelle.p_po4 = self.pns[pns]["p_ges"].get()
                meine_probenahmestelle.save()
                return True
            except:
                return False
        elif pns <= 8:
            try:
                # Passende Probenahmestelle zur KA und zur Stelle aus der DB holen oder erstellen
                meine_probenahmestelle = db.probe_schlamm_asche.objects.get_or_create(klaeranlage = self.ds, probe_probenahmestelle_id = pns)[0]
                meine_probenahmestelle.menge = self.pns[pns]["menge"].get()
                meine_probenahmestelle.p_ges_massenanteil = self.pns[pns]["p_ges_massenanteil"].get()
                meine_probenahmestelle.save()
                return True
            except:
                return False
        else:
            return False

    # Fkt schreibt alle Probenahmestellen in DB
    # self.ds muss vorher schon auf den richtigen DS gesetzt sein!
    def speicher_alle_probenahmestellen(self):
        for i in [1, 2, 3, 4, 5, 6, 7, 8]:
            if not self.speicher_probenahmestelle(i):
                return False
        return True

    # Fkt schreibt Verfahren Ablauf Daten in die DB
    # self.ds muss vorher schon auf den richtigen DS gesetzt sein!
    def speicher_verfahren_ablauf(self):
        try:
            # Passendes Verfahren aus der Datenbank holen
            mein_verf = self.ds.verfahren_ablauf.objects.get_or_create(klaeranlage = self.ds)[0]
            mein_verf.p_prozent_entnahme = self.verf_ablauf["p_prozent_entnahme"].get()
            mein_verf.investkosten = self.verf_ablauf["investkosten"].get()
            mein_verf.betriebskosten_pro_p = self.verf_ablauf["betriebskosten_pro_p"].get()
            mein_verf.verkaufserloes_pro_p = self.verf_ablauf["verkaufserloes_pro_p"].get()
            mein_verf.zeitspanne_abschreibung = self.verf_ablauf["zeitspanne_abschreibung"].get()
            mein_verf.save()
            return True
        except:
            return False

    # Fkt schreibt Verfahren Schlammwasser Daten in die DB
    # self.ds muss vorher schon auf den richtigen DS gesetzt sein!
    def speicher_verfahren_schlammwasser(self):
        try:
            # Passendes Verfahren aus der Datenbank holen
            mein_verf = self.ds.verfahren_schlammwasser.objects.get_or_create(klaeranlage = self.ds)[0]
            mein_verf.p_prozent_entnahme = self.verf_schlammwasser["p_prozent_entnahme"].get()
            mein_verf.investkosten = self.verf_schlammwasser["investkosten"].get()
            mein_verf.betriebskosten_pro_p = self.verf_schlammwasser["betriebskosten_pro_p"].get()
            mein_verf.verkaufserloes_pro_p = self.verf_schlammwasser["verkaufserloes_pro_p"].get()
            mein_verf.zeitspanne_abschreibung = self.verf_schlammwasser["zeitspanne_abschreibung"].get()
            mein_verf.n_nh4_vorher = self.verf_schlammwasser["n_nh4_vorher"].get()
            mein_verf.n_nh4_prozent_entnahme = self.verf_schlammwasser["n_nh4_prozent_entnahme"].get()
            mein_verf.save()
            return True
        except:
            return False

    # Fkt schreibt Verfahren Faulschlamm Daten in die DB
    # self.ds muss vorher schon auf den richtigen DS gesetzt sein!
    def speicher_verfahren_faulschlamm(self):
        try:
            # Passendes Verfahren aus der Datenbank holen
            mein_verf = self.ds.verfahren_faulschlamm.objects.get_or_create(klaeranlage = self.ds)[0]
            mein_verf.p_prozent_entnahme = self.verf_faulschlamm["p_prozent_entnahme"].get()
            mein_verf.investkosten = self.verf_faulschlamm["investkosten"].get()
            mein_verf.betriebskosten_pro_p = self.verf_faulschlamm["betriebskosten_pro_p"].get()
            mein_verf.verkaufserloes_pro_p = self.verf_faulschlamm["verkaufserloes_pro_p"].get()
            mein_verf.zeitspanne_abschreibung = self.verf_faulschlamm["zeitspanne_abschreibung"].get()
            mein_verf.kosten_schlammentsorgung = self.verf_faulschlamm["kosten_schlammentsorgung"].get()
            mein_verf.n_nh4_vorher = self.verf_faulschlamm["n_nh4_vorher"].get()
            mein_verf.n_nh4_prozent_entnahme = self.verf_faulschlamm["n_nh4_prozent_entnahme"].get()
            mein_verf.save()
            return True
        except:
            return False

    # Fkt schreibt Verfahren Asche Daten in die DB
    # self.ds muss vorher schon auf den richtigen DS gesetzt sein!
    def speicher_verfahren_asche(self):
        try:
            # Passendes Verfahren aus der Datenbank holen
            mein_verf = self.ds.verfahren_asche.objects.get_or_create(klaeranlage = self.ds)[0]
            mein_verf.p_prozent_entnahme = self.verf_asche["p_prozent_entnahme"].get()
            mein_verf.investkosten = self.verf_asche["investkosten"].get()
            mein_verf.betriebskosten_pro_p = self.verf_asche["betriebskosten_pro_p"].get()
            mein_verf.verkaufserloes_pro_p = self.verf_asche["verkaufserloes_pro_p"].get()
            mein_verf.zeitspanne_abschreibung = self.verf_asche["zeitspanne_abschreibung"].get()
            mein_verf.kosten_schlammverbrennung = self.verf_asche["kosten_schlammverbrennung"].get()
            mein_verf.save()
            return True
        except:
            return False

    # Fkt schreibt alle Verfahren in die DB
    # self.ds muss vorher schon auf den richtigen DS gesetzt sein!
    def speicher_alle_verfahren(self):
        if not self.speicher_verfahren_ablauf():
            return False
        if not self.speicher_verfahren_schlammwasser():
            return False
        if not self.speicher_verfahren_faulschlamm():
            return False
        if not self.speicher_verfahren_asche():
            return False
        return True

    # Fkt lädt Kläranlagen-Tabelle aus DB
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_klaeranlage(self):
        try:
            self.abwasserabgabe_n.set(self.ds.abwasserabgabe_n)
            self.abwasserabgabe_p.set(self.ds.abwasserabgabe_p)
            self.kosten_schlammentsorgung.set(self.ds.kosten_schlammentsorgung)
            self.ort.set(self.ds.ort.ort)
            return True
        except:
            return False

    # Fkt lädt Probe zu Probenahmestelle 1-6, aber nur eine!
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_probe_fluessig(self, stelle = 0):
        if stelle <= 0:
            return False
        # Nur wenn die Probenahme stelle 1-6 ist etwas tun
        elif stelle <= 6:
            try:
                # Passende Probe aus der Datenbank holen
                meine_probe = self.ds.probe_fluessig_set.filter(probe_probenahmestelle_id = stelle)[0]
                self.pns[stelle]["p_ges"].set(meine_probe.p_ges)
                self.pns[stelle]["p_po4"].set(meine_probe.p_po4)
                self.pns[stelle]["durchfluss"].set(meine_probe.durchfluss)
                return True
            except:
                return False
        else:
            return False

    # Fkt lädt Probe zu Probenahmestelle 7-8, aber nur eine!
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_probe_schlamm_asche(self, stelle = 0):
        if stelle <= 6:
            return False
        elif stelle <= 8:
            try:
                # Passende Probe aus der Datenbank holen
                meine_probe = self.ds.probe_schlamm_asche_set.filter(probe_probenahmestelle_id = stelle)[0]
                self.pns[stelle]["menge"].set(meine_probe.menge)
                self.pns[stelle]["p_ges_massengehalt"].set(meine_probe.p_ges_massengehalt)
                return True
            except:
                return False
        else:
            return False

    # Fkt lädt Probe zu einzelner Probenahmestelle aus der DB
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_probe(self, stelle = 0):
        # Falls nichts angegeben
        if stelle <= 0:
            return False
        # Falls flüssige Probe
        elif stelle <= 6:
            return self.lade_probe_fluessig(stelle = stelle)
        # Falls nicht flüssige Probe
        elif stelle <= 8:
            return self.lade_probe_schlamm_asche(stelle = stelle)
        else:
            return False

    # Fkt lädt alle Proben an allen Probenahmestellen aus der DB
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_alle_proben(self):
        for x in [1, 2, 3, 4, 5, 6, 7, 8]:
            rueck = self.lade_probe(stelle = x)
            if not rueck:
                return False
        return True

    # Fkt lädt Verfahren Ablauf Daten aus der DB
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_verfahren_ablauf(self):
        # Passendes Verfahren aus der Datenbank holen
        mein_verf = self.ds.verfahren_ablauf_set.all()[0]
        self.verf_ablauf["p_prozent_entnahme"].set(mein_verf.p_prozent_entnahme)
        self.verf_ablauf["investkosten"].set(mein_verf.investkosten)
        self.verf_ablauf["betriebskosten_pro_p"].set(mein_verf.betriebskosten_pro_p)
        self.verf_ablauf["verkaufserloes_pro_p"].set(mein_verf.verkaufserloes_pro_p)
        self.verf_ablauf["zeitspanne_abschreibung"].set(mein_verf.zeitspanne_abschreibung)

    # Fkt lädt Verfahren Schlammwasser Daten aus der DB
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_verfahren_schlammwasser(self):
        # Passendes Verfahren aus der Datenbank holen
        mein_verf = self.ds.verfahren_schlammwasser_set.all()[0]
        self.verf_schlammwasser["p_prozent_entnahme"].set(mein_verf.p_prozent_entnahme)
        self.verf_schlammwasser["investkosten"].set(mein_verf.investkosten)
        self.verf_schlammwasser["betriebskosten_pro_p"].set(mein_verf.betriebskosten_pro_p)
        self.verf_schlammwasser["verkaufserloes_pro_p"].set(mein_verf.verkaufserloes_pro_p)
        self.verf_schlammwasser["zeitspanne_abschreibung"].set(mein_verf.zeitspanne_abschreibung)
        self.verf_schlammwasser["n_nh4_vorher"].set(mein_verf.n_nh4_vorher)
        self.verf_schlammwasser["n_nh4_prozent_entnahme"].set(mein_verf.n_nh4_prozent_entnahme)

    # Fkt lädt Verfahren Faulschlamm Daten aus der DB
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_verfahren_faulschlamm(self):
        # Passendes Verfahren aus der Datenbank holen
        mein_verf = self.ds.verfahren_faulschlamm_set.all()[0]
        self.verf_faulschlamm["p_prozent_entnahme"].set(mein_verf.p_prozent_entnahme)
        self.verf_faulschlamm["investkosten"].set(mein_verf.investkosten)
        self.verf_faulschlamm["betriebskosten_pro_p"].set(mein_verf.betriebskosten_pro_p)
        self.verf_faulschlamm["verkaufserloes_pro_p"].set(mein_verf.verkaufserloes_pro_p)
        self.verf_faulschlamm["zeitspanne_abschreibung"].set(mein_verf.zeitspanne_abschreibung)
        self.verf_faulschlamm["kosten_schlammentsorgung"].set(mein_verf.kosten_schlammentsorgung)
        self.verf_faulschlamm["n_nh4_vorher"].set(mein_verf.n_nh4_vorher)
        self.verf_faulschlamm["n_nh4_prozent_entnahme"].set(mein_verf.n_nh4_prozent_entnahme)

    # Fkt lädt Verfahren Asche Verfahren aus der DB
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_verfahren_asche(self):
        # Passendes Verfahren aus der Datenbank holen
        mein_verf = self.ds.verfahren_asche_set.all()[0]
        self.verf_asche["p_prozent_entnahme"].set(mein_verf.p_prozent_entnahme)
        self.verf_asche["investkosten"].set(mein_verf.investkosten)
        self.verf_asche["betriebskosten_pro_p"].set(mein_verf.betriebskosten_pro_p)
        self.verf_asche["verkaufserloes_pro_p"].set(mein_verf.verkaufserloes_pro_p)
        self.verf_asche["zeitspanne_abschreibung"].set(mein_verf.zeitspanne_abschreibung)
        self.verf_asche["kosten_schlammverbrennung"].set(mein_verf.kosten_schlammverbrennung)

    # Fkt lädt alle Verfahren aus der DB
    # in self.ds muss schon der richtige Datensatz geladen sein
    def lade_alle_verfahren(self):
        try:
            # Lade Verfahrensdaten für das Verfahren Ablauf
            if not self.lade_verfahren_ablauf():
                return False
            # Lade Verfahrensdaten für das Verfahren Schlammwasser
            if not self.lade_verfahren_schlammwasser():
                return False
            # Lade Verfahrensdaten für das Verfahren Faulschlamm
            if not self.lade_verfahren_faulschlamm():
                return False
            # Lade Verfahrensdaten für das Verfahren Asche
            if not self.lade_verfahren_asche():
                return False
            return True
        except:
            return False

    # Funktion setzt aktuellen Datensatz auf den zuletzt aktiven und alle anderen zurück
    def setze_aktiv(self):
        # Alle KA Datensätze heraus holen und auf nicht-aktiv setzen und speichern
        ka = db.Klaeranlage.objects.all()
        ka.update(zuletzt_aktiv = False)
        ka.save()
        # Aktuellen Datensatz heraus holen und auf aktiv setzen und speichern
        diese_ka = ka.filter(id = self.id)
        diese_ka.zuletzt_aktiv = True
        diese_ka.save()

    # CSV Zeile aus einem einzelnen KA-Datensatz bauen
    def csv_zeile_aus_ds(self, klaeranlage):
        rueckgabe_string = str(klaeranlage.id) +";" +\
            klaeranlage.ort.ort + ";" +\
            dez_str(klaeranlage.abwasserabgabe_p) + ";" +\
            dez_str(klaeranlage.abwasserabgabe_n) + ";" +\
            dez_str(klaeranlage.kosten_schlammentsorgung) + ";"
        # Alle Probenahmestellen durch iterieren
        for i in  [1, 2, 3, 4, 5, 6]:
            rueckgabe_string += str_dez(klaeranlage.probe_fluessig_set.filter(probe_probenahmestelle_id = i)[0].durchfluss) +\
                ";" + str_dez(klaeranlage.probe_fluessig_set.filter(probe_probenahmestelle_id = i)[0].p_ges) + ";" +\
                str_dez(klaeranlage.probe_fluessig_set.filter(probe_probenahmestelle_id = i)[0].po4) + ";"
        for i in [7, 8]:
            rueckgabe_string += str_dez(klaeranlage.probe_schlamm_asche_set.filter(probe_probenahmestelle_id = i)[0].menge) +\
                ";" + str_dez(klaeranlage.probe_schlamm_asche_set.filter(probe_probenahmestelle_id = i)[0].p_ges) + ";"

        # Verfahren Ablauf in CSV-String konvertieren
        rueckgabe_string += str_dez(klaeranlage.verfahren_ablauf_set.all()[0].p_prozent_entnahme) + ";" +\
            str_dez(klaeranlage.verfahren_ablauf_set.all()[0].investkosten) + ";" +\
            str_dez(klaeranlage.verfahren_ablauf_set.all()[0].betriebskosten_pro_p) + ";" +\
            str_dez(klaeranlage.verfahren_ablauf_set.all()[0].verkaufserloes_pro_p) + ";" +\
            str_dez(klaeranlage.verfahren_ablauf_set.all()[0].zeitspanne_abschreibung) + ";"

        # Verfahren Schlammwasser in CSV-String konvertieren
        rueckgabe_string += str_dez(klaeranlage.verfahren_schlammwasser_set.all()[0].p_prozent_entnahme) + ";" +\
            str_dez(klaeranlage.verfahren_schlammwasser_set.all()[0].investkosten) + ";" +\
            str_dez(klaeranlage.verfahren_schlammwasser_set.all()[0].betriebskosten_pro_p) + ";" +\
            str_dez(klaeranlage.verfahren_schlammwasser_set.all()[0].verkaufserloes_pro_p) + ";" +\
            str_dez(klaeranlage.verfahren_schlammwasser_set.all()[0].zeitspanne_abschreibung) + ";" +\
            str_dez(klaeranlage.verfahren_schlammwasser_set.all()[0].n_nh4_vorher) + ";" +\
            str_dez(klaeranlage.verfahren_schlammwasser_set.all()[0].n_nh4_prozent_entnahme) + ";"

        #Verfahren Faulschlamm in CSV-String konvertieren
        rueckgabe_string += str_dez(klaeranlage.verfahren_faulschlamm_set.all()[0].p_prozent_entnahme) + ";" +\
            str_dez(klaeranlage.verfahren_faulschlamm_set.all()[0].investkosten) + ";" +\
            str_dez(klaeranlage.verfahren_faulschlamm_set.all()[0].betriebskosten_pro_p) + ";" +\
            str_dez(klaeranlage.verfahren_faulschlamm_set.all()[0].verkaufserloes_pro_p) + ";" +\
            str_dez(klaeranlage.verfahren_faulschlamm_set.all()[0].zeitspanne_abschreibung) + ";" +\
            str_dez(klaeranlage.verfahren_faulschlamm_set.all()[0].kosten_schlammentsorgung) + ";" +\
            str_dez(klaeranlage.verfahren_faulschlamm_set.all()[0].n_nh4_vorher) + ";" +\
            str_dez(klaeranlage.verfahren_faulschlamm_set.all()[0].n_nh4_prozent_entnahme) + ";"

        #Verfahren Asche in CSV-String konvertieren
        rueckgabe_string += str_dez(klaeranlage.verfahren_asche_set.all()[0].p_prozent_entnahme) + ";" +\
            str_dez(klaeranlage.verfahren_asche_set.all()[0].investkosten) + ";" +\
            str_dez(klaeranlage.verfahren_asche_set.all()[0].betriebskosten_pro_p) + ";" +\
            str_dez(klaeranlage.verfahren_asche_set.all()[0].verkaufserloes_pro_p) + ";" +\
            str_dez(klaeranlage.verfahren_asche_set.all()[0].zeitspanne_abschreibung) + ";" +\
            str_dez(klaeranlage.verfahren_asche_set.all()[0].kosten_schlammverbrennung) + ";"

        return rueckgabe_string

    # Aus allen verfügbaren KA-Datensätzen in der DB einen CSV-Block erstellen
    def csv_inhalt_aus_allen_ds(self):
        # alle KA ausser der ersten aus der DB holen
        alle_ka = db.Klaeranlage.objects.all().select_related('ort', 'probe_fluessig', 'probe_schlamm_asche',
            'probenahmestelle', 'verfahren_ablauf', 'verfahren_asche', 'verfahren_faulschlamm',
            'verfahren_schlammwasser', 'zeitspanne')#.exclude(id = 1)

        csv_string = []
        # Aus jeder Kläranlage eine CSV-Zeile erstellen und aneinander hängen
        for jede_ka in alle_ka:
            csv_string.append(self.csv_zeile_aus_ds((jede_ka)))
        return csv_string

    # CSV-File schreiben mit Spaltenüberschriften und kompletter DB als Inhalt
    def schreibe_csv_datei(self, dateiname):
        titelzeile = "ID;Name der Kläranlage;Ort;Abwasserabgabe Phosphor [€/kg];Abwasserabgabe N [€/kg];" +\
            "Kosten Schlammentsorgung [€/t];PNS 1 Durchfluss [m³/a];PNS 1 P_ges [kg/a];PNS 1 P_PO4 [kg/a];" +\
            "PNS 2 Durchfluss [m³/a];PNS 2 P_ges [kg/a];PNS 2 P_PO4 [kg/a];PNS 3 Durchfluss [m³/a];PNS 3 P_ges [kg/a];"+\
            "PNS 3 P_PO4 [kg/a];PNS 4 Durchfluss [m³/a];PNS 4 P_ges [kg/a];PNS 4 P_PO4 [kg/a];PNS 5 Durchfluss [m³/a];"+\
            "PNS 5 P_ges [kg/a];PNS 5 P_PO4 [kg/a];PNS 6 Durchfluss [m³/a];PNS 6 P_ges [kg/a];PNS 6 P_PO4 [kg/a];"+\
            "PNS 7 Menge [t/a];PNS 7 P_ges Prozent Massengehalt [%];PNS 8 Menge [t/a];"+\
            "PNS 8 P_ges Prozent Massengehalt[%];Verfahren KA Ablauf Prozent P-Entnahme [%];"+\
            "Verfahren KA Ablauf Investkosten [€];Verfahren KA Ablauf Betriebskosten pro Jahr pro kg P[€/a/kg P];"+\
            "Verfahren KA Ablauf Verkaufserlös [€/kg P];Verfahren KA Ablauf Abschreibungszeitspanne [a];"+\
            "Verfahren Schlammwasser Prozent P-Entnahme [%];Verfahren Schlammwasser Investkosten [€];"+\
            "Verfahren Schlammwasser Betriebskosten pro Jahr pro kg P[€/a/kg P];"+\
            "Verfahren Schlammwasser Verkaufserlös [€/kg P];Verfahren Schlammwasser Abschreibungszeitspanne [a];"+\
            "Verfahren Schlammwasser N_NH4 Vorher [kg/a];Verfahren Schlammwasser Prozent N_NH4 Entnahme [%];"+\
            "Verfahren Faulschlamm Prozent P-Entnahme [%];Verfahren Faulschlamm Investkosten [€];"+\
            "Verfahren Faulschlamm Betriebskosten pro Jahr pro kg P[€/a/kg P];"+\
            "Verfahren Faulschlamm Verkaufserlös [€/kg P];Verfahren Faulschlamm Abschreibungszeitspanne [a];"+\
            "Verfahren Faulschlamm Kosten Schlammentsorgung [€/t];Verfahren Faulschlamm N_NH4 Vorher [kg/a];"+\
            "Verfahren Faulschlamm Prozent N_NH4 Entnahme [%];Verfahren Asche Prozent P-Entnahme [%];"+\
            "Verfahren Asche Investkosten [€];Verfahren Asche Betriebskosten pro Jahr pro kg P[€/a/kg P];"+\
            "Verfahren Asche Verkaufserlös [€/kg P];Verfahren Asche Abschreibungszeitspanne [a];"+\
            "Verfahren Asche Kosten Schlammverbrennung [€/t]\r\n"
        # Aufhören wenn es die Datei schon gibt oder GUI-Abfrage ob überschrieben werden soll
        # Falls es das File schon gibt aufhören
        if os.path.isfile(dateiname):
            self.statuszeile.set("Datei "+dateiname+" existiert schon, wird nicht überschrieben")
            return False
        # Falls es das File noch nicht gibt weiter machen

        # CSV-Inhalt aus allen Datensätzen holen
        inhalt_csv = self.csv_inhalt_aus_allen_ds()

        # Komplette Datenbank ausser Default-Datensatz in ein CSV mit Titelzeile schreiben
        offene_datei = open(dateiname, "rw")
        offene_datei.writelines(titelzeile)
        offene_datei.writelines(inhalt_csv)
        offene_datei.close()


    # Aus einer CSV-Datei Datensätze lesen
    def lese_csv_datei(self, dateiname):
        # Checken ob es das File überhaupt gibt -> sonst Fehler in Statuszeile und
        # Erst checken ob das File dem gewünschten Format entspricht!
        # Wenn nicht wenn möglich sagen in welcher Zeile ein Fehler ist

        # Tu Dinge
        pass