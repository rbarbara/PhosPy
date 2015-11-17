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

# GUI importieren
#import gui as gui



# GUI erst mal hier, auslagern später
# Hauptfenster
root_Fenster = tk.Frame(height = 786, width = 1024)
root_Fenster.master.title("PhosPy")

# Root Fenster auf Größe festlegen und zeichnen lassen
root_Fenster.grid_propagate(0)
root_Fenster.grid()


hauptmenue = ttk.Menubutton(root_Fenster,text = "Test" )



# GUI Starten
root_Fenster.mainloop()



