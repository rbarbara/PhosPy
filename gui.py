#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
import sys

#Grafik Toolkit importieren
import Tkinter as tk

# Django-Datenbank importieren
import db.models as db

