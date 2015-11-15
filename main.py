#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
import sys

import db.models as db
