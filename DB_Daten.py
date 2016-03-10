#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
import sys

# Django-Datenbank importieren
import db.models as db

# Grafik Toolkit imporotieren
import tkinter as tk
import tkinter.ttk as ttk

# Default-Werte importieren
import Default_Werte as default

# Damit das tut... ohne gehen die Special-Gui-Vars nicht
root = tk.Tk()


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
        self.kosten_Schlammentsorgung = tk.DoubleVar(default.KOSTEN_SCHLAMMENTSORGUNG)

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


        self.statuszeile.set("Initialisieren fertig")

        #self.lade_Datensatz()

        # Daten_berechnen

    # Fkt lädt einen bestimmten Datensatz
    def lade_datensatz(self, ka_id = 1):
        pass
        # Am Ende Statuszeile auf "Datensatz Nr. bla geladen"
        # Testen ob es den Datensatz überhaupt gibt:
        try:
            self.ds = db.Klaeranlage.objects.filter(id = ka_id).select_related('ort', 'probe_fluessig', 'probe_schlamm_asche',
                'probenahmestelle', 'verfahren_ablauf', 'verfahren_asche', 'verfahren_faulschlamm',
                'verfahren_schlammwasser', 'zeitspanne')[0]

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
    def lade_letzten_aktiven_Datensatz(self):
        try:
            # Alle Datensätze mit dem aktive-Flag heraus holen
            aktive_ds = db.Klaeranlage.objects.filter(zuletzt_aktiv = True)
            # Falls es mehrere Datensätze mit dem "zuletzt_aktiv" Flag gibt den ersten nehmen und die anderen zurück setzen
            if aktive_ds.count() != 1:
                aktive_ds.update(zuletzt_aktiv = False)
                aktive_ds[0].zuletzt_aktiv = True
                aktive_ds.save()
            # Datensatz ID an die laden-Fkt übergeben
            return self.lade_Datensatz(ka_id = aktive_ds[0].id)
        except:
            return False

    # Funktion speichert den aktiven Datensatz als neuen Datensatz oder überschreibt einen alten je nach dem Flag "ueberschreiben"
    # id_ueberschreiben wird ignoriert wenn ueberschreiben = False
    def speicher_Datensatz(self, ueberschreiben = False):
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
    def __new__():
        try:
            mein_ort = db.Ort.objects.create(ort = "Default Ort")
            mein_ort.save()
            meine_ka = db.Klaeranlage.objects.create(ort = mein_ort)
            meine_ka.save()
            meine_id = meine_ka.id
            mein_verf_abl = db.verfahren_ablauf.objects.create(klaeranlage = meine_ka, ansatzpunkt_id = 3)
            mein_verf_abl.save()
            mein_verf_schlw = db.verfahren_schlammwasser.objects.create(klaeranlage = meine_ka, ansatzpunkt_id = 2)
            mein_verf_schlw.save()
            mein_verf_faulschl = db.verfahren_faulschlamm.objects.create(klaeranlage = meine_ka, ansatzpunkt_id = 6)
            mein_verf_faulschl.save()
            mein_verf_asche = db.verfahren_asche.objects.create(klaeranlage = meine_ka, ansatzpunkt_id = 8)
            mein_verf_asche.save()
            for i in [1, 2, 3, 4, 5, 6]:
                meine_probenahmestelle = db.probe_fluessig.objects.create(klaeranlage = meine_ka, probe_probenahmestelle_id = i)
                meine_probenahmestelle.save()
            for i in [7, 8]:
                meine_probenahmestelle = db.probe_schlamm_asche.objects.create(klaeranlage = meine_ka, probe_probenahmestelle = i)
                meine_probenahmestelle.save()
            self.id = meine_ka.id
            return meine_id
        except:
            return False

    # Einmal alles berechnen neu Triggern
    def alles_berechnen(self):
        # Tu Dinge
        pass

    # Aus einer CSV-Datei Datensätze lesen
    def lese_csv_datei(self, dateiname):
        # Checken ob es das File überhaupt gibt -> sonst Fehler in Statuszeile und
        # Erst checken ob das File dem gewünschten Format entspricht!
        # Wenn nicht wenn möglich sagen in welcher Zeile ein Fehler ist
        # Tu Dinge
        pass

    def schreibe_csv_datei(self, dateiname):
        # Aufhören wenn es die Datei schon gibt oder GUI-Abfrage ob überschrieben werden soll

        # Komplette Datenbank ausser Default-Datensatz in ein CSV mit Titelzeile schreiben

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
            mein_verf.p_prozent_entnahme = self.verf_ablauf["p_prozent_entnahme"].get()
            mein_verf.investkosten = self.verf_ablauf["investkosten"].get()
            mein_verf.betriebskosten_pro_p = self.verf_ablauf["betriebskosten_pro_p"].get()
            mein_verf.verkaufserloes_pro_p = self.verf_ablauf["verkaufserloes_pro_p"].get()
            mein_verf.zeitspanne_abschreibung = self.verf_ablauf["zeitspanne_abschreibung"].get()
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
            mein_verf.p_prozent_entnahme = self.verf_ablauf["p_prozent_entnahme"].get()
            mein_verf.investkosten = self.verf_ablauf["investkosten"].get()
            mein_verf.betriebskosten_pro_p = self.verf_ablauf["betriebskosten_pro_p"].get()
            mein_verf.verkaufserloes_pro_p = self.verf_ablauf["verkaufserloes_pro_p"].get()
            mein_verf.zeitspanne_abschreibung = self.verf_ablauf["zeitspanne_abschreibung"].get()
            mein_verf.kosten_schlammentsorgung = self.verf_faulschlamm["kosten_schlammentsorgung"].get()
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
            mein_verf.p_prozent_entnahme = self.verf_ablauf["p_prozent_entnahme"].get()
            mein_verf.investkosten = self.verf_ablauf["investkosten"].get()
            mein_verf.betriebskosten_pro_p = self.verf_ablauf["betriebskosten_pro_p"].get()
            mein_verf.verkaufserloes_pro_p = self.verf_ablauf["verkaufserloes_pro_p"].get()
            mein_verf.zeitspanne_abschreibung = self.verf_ablauf["zeitspanne_abschreibung"].get()
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
