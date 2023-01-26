# This file contains the WSGI configuration required to serve up your
# web application at http://Uoyroem.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Django project

from django.core.wsgi import get_wsgi_application
import os
import sys

# add your project directory to the sys.path
project_home = '/home/Uoyroem/stack'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'


# serve django via WSGI
application = get_wsgi_application()
