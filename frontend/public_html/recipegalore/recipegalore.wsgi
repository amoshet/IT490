#!/usr/bin/python3.8
import sys
sys.path.insert(0,"/home/ahmed_moshet/IT490/frontend/public_html/recipegalore")

from recipegalore import app as application
application.secret_key = 'shh'
