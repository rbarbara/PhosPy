#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME' : os.path.join(BASE_DIR, 'db.sqlite3'), 
        'HOST' : '',
        'USER' : '', 
        'PASSWORD' : '', 
        'PORT' : ''
        }
    }
    
SECRET_KEY = 'meinsecretkey'

INSTALLED_APPS = (
    'db',
    )
