#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
import sys

# Grafik Toolkit imporotieren
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font

# Django-Datenbank importieren
import db.models as db

import DB_Daten as dbd

root = tk.Tk()

# Hauptfenster
"""
das = dbd.KA_Datensatz()

print(das.pns[1]["durchfluss"].get())
print(das.statuszeile.get())

print(type(das))
"""

class Foo():
    def __init__(self):
        self.bar = tk.StringVar()
        self.bar.set("Init!")

    def get_bar(self):
        return self.bar.get()

    def set_bar(self, sth):
        self.bar.set(sth)

    bar = property(get_bar, set_bar)


irgendwas = Foo()
print (irgendwas.bar)
irgendwas.bar = "Hallo"
print(irgendwas.bar)
