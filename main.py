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

# Größe unveränderbar
root_Fenster.resizable(width = None, height = None)

root_Fenster.mainloop()




"""

root_Tk.configure(height = 786, width = 1024)

# Titel Hauptfenster
root_Tk.title("PhosPy")

# Größe unveränderbar
root_Tk.resizable(width = None, height = None)


# Hauptmenü-Zeile ==============================================================
hauptmenue_Zeile = tk.Menu(root_Tk, tearoff = 0)
#hauptmenue_Zeile.grid(row = 0)
root_Tk.config(menu = hauptmenue_Zeile)
#root_Tk.grid()


# Erstes Untermenü =============================================================
menue_Datei = tk.Menu(master = hauptmenue_Zeile, tearoff = 0)

# erstes Untermenü zu Hauptmenü hinzufügen
hauptmenue_Zeile.add_cascade(label = "Datei", menu = menue_Datei)

# Bausteine in erstes Untermenü hinzufügen
menue_Datei.add_command(label = "Neues irgendwas", command = machNix)
menue_Datei.add_command(label = "Speichern", command = machNix)
menue_Datei.add_command(label = "Öffnen", command = machNix)
menue_Datei.add_separator()
menue_Datei.add_command(label = "Schließen", command = root_Tk.quit)


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

#Bausteine in erstes Untermenü hinzufügen
for jeden in styles_Liste:
    menue_Styles.add_radiobutton(label = jeden, value = jeden, variable = gewaehlter_Style, command = checkStyle)

# viertes Untermenü zu Hauptmenü hinzufügen
hauptmenue_Zeile.add_cascade(label = "Styles", menu = menue_Styles)

# Frame in der Mitte
haupt_Frame = ttk.Frame(master = root_Tk)
haupt_Frame.grid()

irgendein_Frame = ttk.Frame(master = haupt_Frame)
irgendein_Frame.grid(row = 0)

irgendein_Label = ttk.Label(master = irgendein_Frame, text = "Bla bla", borderwidth = 1)
irgendein_Label.grid()




# Statuszeile ==================================================================
inhalt_Statuszeile = tk.StringVar()
inhalt_Statuszeile.set("Hallo, hier sollte ich sein!")
statuszeile = ttk.Label(master = haupt_Frame, textvariable = inhalt_Statuszeile,
                        borderwidth = 1, relief = tk.SUNKEN, justify = tk.LEFT,
                        anchor = tk.S)

statuszeile.grid(sticky = (tk.W, tk.E, tk.S), row = 1)






# ==============================================================================
# GUI Starten
# ==============================================================================

root_Tk.mainloop()




"""