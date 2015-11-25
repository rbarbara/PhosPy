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

# Hauptfenster
