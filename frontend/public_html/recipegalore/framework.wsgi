#!/usr/bin/python
import sys
sys.path.insert(0,"/IT490/frontend/public_html/")

activate_this = '/home/ahmed_moshet/.local/share/virtualenvs/recipegalore-tsT3ZzLA/bin/activate_this.py'
with open(activate_this) as file_:
    exect(file_.read(), dict(__file__=activate_this))

from framework import app as application
