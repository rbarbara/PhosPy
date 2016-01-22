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
import tkinter.font as font

# GUI importieren
#import gui as gui

# GUI-Text-Funktion
def machNix():
    print("Nix gemacht!")

# Funktion für das Styles Menü
def checkStyle():
    # Auf den gewaehlten Sytle per globaler Variable zugreifen
    global gewaehlter_Style
    print(gewaehlter_Style.get())
    style = ttk.Style()
    style.theme_use(gewaehlter_Style.get())




# ==============================================================================
# GUI Initialisierung
# ==============================================================================

# Tk-Hauptfenster ==============================================================
# Das Hauptfenster hat keinen Master!
# Breite 1024 Pixel und  Höhe 786 Pixel
root_Fenster = tk.Tk()
root_Fenster.configure(width = 1024, height = 786)

# Titel Hauptfenster
root_Fenster.title("PhosPy")

# Größe unveränderbar, Min und Max-Größe festlegen auf gleiche Größe
root_Fenster.minsize(width = 1024, height = 786)
root_Fenster.maxsize(width = 1024, height = 786)

# Hauptmenü-Zeile ==============================================================
# Oberste Zeile ist die Hauptmenü-Zeile
hauptmenue_Zeile = tk.Menu(root_Fenster, tearoff = False)

# Dem root-Fenster die Menü-Zeile bekannt machen
root_Fenster.configure(menu = hauptmenue_Zeile)

# Erstes Untermenü =============================================================
menue_Datei = tk.Menu(master = hauptmenue_Zeile, tearoff = 0)

# erstes Untermenü zu Hauptmenü hinzufügen
hauptmenue_Zeile.add_cascade(label = "Datei", menu = menue_Datei)

# Bausteine in erstes Untermenü hinzufügen
menue_Datei.add_command(label = "Neues irgendwas", command = machNix)
menue_Datei.add_command(label = "Speichern", command = machNix)
menue_Datei.add_command(label = "Öffnen", command = machNix)
menue_Datei.add_separator()
menue_Datei.add_command(label = "Schließen", command = root_Fenster.quit)


# Zweites Untermenü ============================================================
menue_Import = tk.Menu(master = hauptmenue_Zeile, tearoff = 0)

# zweites Unteremnü zu Hauptmenü hinzufügen
hauptmenue_Zeile.add_cascade(label = "Import", menu = menue_Import)

#Bausteine in erstes Untermenü hinzufügen
menue_Import.add_command(label = "Import von CSV")


# Drittes Untermenü ============================================================
menue_Export = tk.Menu(master = hauptmenue_Zeile, tearoff = 0)

# drittes Unteremnü zu Hauptmenü hinzufügen
hauptmenue_Zeile.add_cascade(label = "Export", menu = menue_Export)

#Bausteine in drittes Untermenü hinzufügen
menue_Export.add_command(label = "Export in CSV")


# Viertes Untermenü ============================================================
menue_Styles = tk.Menu(master = hauptmenue_Zeile, tearoff = 0)

# Auslesen welche Styles auf dem Menü verfügbar sind
styles = ttk.Style()
styles_Liste = []
styles_Liste = styles.theme_names()
gewaehlter_Style = tk.StringVar()
gewaehlter_Style.set("default")

#Bausteine im vierten Untermenü hinzufügen
for jeden in styles_Liste:
    menue_Styles.add_radiobutton(label = jeden, value = jeden, variable = gewaehlter_Style, command = checkStyle)

# viertes Untermenü zu Hauptmenü hinzufügen
hauptmenue_Zeile.add_cascade(label = "Styles", menu = menue_Styles)


# Werkzeugleiste ===============================================================
werkzeugleiste = ttk.Frame(master = root_Fenster, borderwidth = 1)
werkzeugleiste.pack(anchor = "n", expand = False, fill = "x", side = "top")

# Notebook-Ansicht =============================================================
Notebook = ttk.Notebook(root_Fenster)

# Durchzappen per Tasten erlauben
Notebook.enable_traversal()

# 1. Notebook-Blatt: Übersicht mit Kläranlagen-Schema
KA_uebersicht = ttk.Frame(Notebook)
Notebook.add(KA_uebersicht)
Notebook.tab(0, text = "Übersicht", sticky = tk.N)

# LabelFrames für diverse Anlagenteile
ganze_Anlage = ttk.LabelFrame(KA_uebersicht, text = "Name der aktiven Kläranlage")
# Mechanische Reinigung
mechanische_Reinigung = ttk.LabelFrame(ganze_Anlage, text = "Mechanische Reinigung")
irgendein_Knopf2 = ttk.Button(mechanische_Reinigung, text = "Anzeigehelfer")
irgendein_Knopf2.pack(anchor = "center")
biologische_Reinigung = ttk.LabelFrame(ganze_Anlage, text = "Biologische Reinigung")
irgendein_Knopf3 = ttk.Button(biologische_Reinigung, text = "Anzeigehelfer")
irgendein_Knopf3.pack(anchor = "center")
schlammbehandlung = ttk.LabelFrame(ganze_Anlage, text = "Schlammbehandlung")
irgendein_Knopf4 = ttk.Button(schlammbehandlung, text = "Anzeigehelfer")
irgendein_Knopf4.pack(anchor = "center")
schlammverbrennung = ttk.LabelFrame(ganze_Anlage, text = "Schlammverbrennung")
irgendein_Knopf5 = ttk.Button(schlammverbrennung, text = "Anzeigehelfer")
irgendein_Knopf5.pack(anchor = "center")

#mechanische_Reinigung.pack(anchor = "nw", side = "top", fill = "both", expand = True)
mechanische_Reinigung.grid(column = 0, row = 0, sticky = tk.N + tk.E + tk.S + tk.W)
#biologische_Reinigung.pack(anchor = "ne")
biologische_Reinigung.grid(column = 1, row = 0, columnspan = 2, sticky = tk.N + tk.E + tk.S + tk.W)
#schlammbehandlung.pack(anchor = "sw")
schlammbehandlung.grid(column = 0, row = 1, columnspan = 2, sticky = tk.N + tk.E + tk.S + tk.W)
#schlammverbrennung.pack(anchor = "se")
schlammverbrennung.grid(column = 2, row = 1, sticky = tk.N + tk.E + tk.S + tk.W)


#irgendein_Knopf = ttk.Button(ganze_Anlage, text = "Anzeigehelfer")
#irgendein_Knopf.pack()
ganze_Anlage.pack(anchor = "center", expand = True, fill = "both", side = "top")





# 2. Notebook-Blatt: Liste der Daten
liste = ttk.Frame(Notebook)
Notebook.add(liste)
Notebook.tab(1, text = "Liste")

# 3. Notebook-Blatt: Phosphat-Bilanz
PO4_Bilanz = ttk.Frame(Notebook)
Notebook.add(PO4_Bilanz )
Notebook.tab(2, text = "Phosphatbilanz")

# 4. Notebook-Blatt: DB-Werte
DB_Werte = ttk.Frame(Notebook)
Notebook.add(DB_Werte )
Notebook.tab(3, text = "DB-Werte")

# Treeview missbrauchen für Tabellenansicht
daten_tabelle = ttk.Treeview(DB_Werte, columns = ("Id", "Name", "Ort", "Wert_1", "Wert_2"))
#daten_tabelle.column("#0", width = 0)
daten_tabelle.heading("#1", text = "Id")
daten_tabelle.column("#1", width = 30, anchor = tk.CENTER)
daten_tabelle.heading("#2", text = "Name")
daten_tabelle.heading("#3", text = "Ort")
daten_tabelle.heading("#4", text = "Wert 1")
daten_tabelle.heading("#5", text = "Wert 2")

# Verhindern, dass erste Spalte angezeigt wird
daten_tabelle['show'] = 'headings'

# Holt alle Datensätze aus der DB und packt sie in die "Tabelle"
alle_daten = db.Klaeranlage.objects.all()
for alle in alle_daten:
   daten_tabelle.insert("", "end", text = alle.id, values = (str(alle.id) +" "+ alle.name +" "+ alle.ort +" "+ alle.wert1 +" "+ alle.wert2) )

daten_tabelle.pack(anchor = "n", expand = True, fill = "both", side = "top")



# 5. Notebook-Blatt: Erweitert
Erweitert = ttk.Frame(Notebook)
Notebook.add(Erweitert)
Notebook.tab(4, text = "Erweitert")

# Notebook nach oben packen und nach links und rechts ausdehnen
Notebook.pack(anchor = "n", expand = True, fill = "both", side = "top")
#Notebook.grid(sticky = (tk.W, tk.E, tk.N), row = 0)


# Statuszeile ==================================================================
inhalt_Statuszeile = tk.StringVar()
inhalt_Statuszeile.set("Hallo, hier sollte ich sein! Ich bin die Statuszeile!")
statuszeile = ttk.Label(master = root_Fenster, textvariable = inhalt_Statuszeile,
                        borderwidth = 1, relief = tk.SUNKEN, justify = tk.LEFT,
                        anchor = tk.S)

# Statuszeile nach unten packen udn links und rechts ausdehnen
statuszeile.pack(anchor = "s", expand = False, fill = "x", side = "bottom")
# statuszeile.grid(sticky = (tk.W, tk.E, tk.S), row = 1)


# ==============================================================================
# GUI Starten
# ==============================================================================
root_Fenster.mainloop()

