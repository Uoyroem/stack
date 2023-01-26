from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
import os
import sys

path = os.path.expanduser('~/stack')
if path not in sys.path:
    sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stack.settings'
application = StaticFilesHandler(get_wsgi_application())
