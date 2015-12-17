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

# Notebook-Ansicht =============================================================
Notebook = ttk.Notebook(root_Fenster)

# Durchzappen per Tasten erlauben
Notebook.enable_traversal()


Seite_1 = ttk.Frame(Notebook)
Notebook.add(Seite_1)
Notebook.tab(0, text = "Übersicht", sticky = tk.W)

Seite_2 = ttk.Frame(Notebook)
Notebook.add(Seite_2 )
Notebook.tab(1, text = "Liste")

Seite_3 = ttk.Frame(Notebook)
Notebook.add(Seite_3 )
Notebook.tab(2, text = "Phosphatbilanz")

Seite_4 = ttk.Frame(Notebook)
Notebook.add(Seite_4 )
Notebook.tab(3, text = "DB-Werte")

Seite_5 = ttk.Frame(Notebook)
Notebook.add(Seite_5 )
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
#statuszeile.grid(sticky = (tk.W, tk.E, tk.S), row = 1)







# ==============================================================================
# GUI Starten
# ==============================================================================
root_Fenster.mainloop()


"""

# ==============================================================================
# GUI Starten
# ==============================================================================

root_Tk.mainloop()

"""