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
    def lade_Datensatz(self, ka_id = 1):
        pass
        # Am Ende Statuszeile auf "Datensatz Nr. bla geladen"
        # Testen ob es den Datensatz überhaupt gibt:
        try:
            self.ds = db.Klaeranlage.objects.filter(id = ka_id).select_related('ort', 'probe_fluessig', 'probe_schlamm_asche',
                'probenahmestelle', 'verfahren_ablauf', 'verfahren_asche', 'verfahren_faulschlamm',
                'verfahren_schlammwasser', 'zeitspanne')[0]
            # Tu Dinge
        except:
            self.statuszeile.set("Den angeforderten Datensatz gibt es nicht")
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
    def speicher_Datensatz(self, ueberschreiben = False, id_ueberschreiben = 0):
        # Genannten Datensatz ueberschreiben
        if ueberschreiben:
            try:
                mein_DS = db.Klaeranlage.objects.get(id = id_ueberschreiben)# Checken ob die ID überhaupt existiert
            except:
                status_string = "Datensatz mit der id: " + str(id_ueberschreiben) + " existiert nicht, überschreiben nicht möglich"
                self.statuszeile.set(status_string)

        # Neuen Datensatz bauen
        else:
            pass

    # Einmal alles berechnen neu Triggern
    def alles_berechnen(self):
        # Tu Dinge
        pass

    # Aus einer CSV-Datei Datensätze lesen
    def lese_CSV_Datei(self, dateiname):
        # Checken ob es das File überhaupt gibt -> sonst Fehler in Statuszeile und
        # Erst checken ob das File dem gewünschten Format entspricht!
        # Wenn nicht wenn möglich sagen in welcher Zeile ein Fehler ist
        # Tu Dinge
        pass

    def schreibe_CSV_Datei(self, dateiname):
        # Aufhören wenn es die Datei schon gibt oder GUI-Abfrage ob überschrieben werden soll

        # Komplette Datenbank ausser Default-Datensatz in ein CSV mit Titelzeile schreiben

        pass


    # Funktion schreibt Kläranlagen Datensatz in die DB
    def schreibe_klaeranalge_in_db(self):
        pass

    # Fkt schreibt Probenahmestelle in DB
    def schreibe_probenahmestelle_in_db(self, pns = 0, alle = False):
        pass

    # Fkt schreibt alle Probenahmestellen in DB
    def schreibe_alle_probenahmestellen_in_db(self):
        pass

    # Fkt schreibt Verfahren Ablauf Daten in die DB
    def schreibe_verfahren_ablauf_in_db(self):
        pass

    # Fkt schreibt Verfahren Schlammwasser Daten in die DB
    def schreibe_verfahren_schlammwasser_in_db(self):
        pass

    # Fkt schreibt Verfahren Faulschlamm Daten in die DB
    def schreibe_verfahren_faulschlamm_in_db(self):
        pass

    # Fkt schreibt Verfahren Asche Daten in die DB
    def schreibe_verfahren_asche_in_db(self):
        pass

    # Fkt schreibt alle Verfahren in die DB
    def schreibe_verfahren_in_die_db(self):
        pass

    # Fkt lädt Kläranlagen-Tabelle aus DB
    def lade_klaeranlage(self):
        pass

    # Fkt lädt Probe zu Probenahmestelle 1-6
    def lade_probe_fluessig(self, stelle = 0):
        if stelle == 0:
            return False
        else:
            pass
            # Tu dinge
            return True
            pass

    # Fkt lädt Probe zu Probenahmestelle 7-8
    def lade_probe_schlamm_asche(self, stelle = 0):
        if stelle == 0:
            return False
        else:
            # Tu dinge
            return True
            pass

    # Fkt lädt Probe zu einzelner Probenahmestelle aus der DB
    def lade_probe(self, stelle = 0):
        # False nichts angegeben
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
    def lade_alle_proben(self):
        for x in [1, 2, 3, 4, 5, 6, 7, 8]:
            rueck = self.lade_probe()
            if not rueck:
                return False
        return True
