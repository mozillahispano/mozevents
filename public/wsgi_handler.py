#
#	Link between django and apache
#
import os, sys 

apache_configuration= os.path.dirname(__file__) 
project = os.path.dirname(apache_configuration) 
workspace = os.path.dirname(project) 

sys.path.append(workspace)

sys.path.append('/usr/lib/pymodules/python2.6/django/') 

sys.path.append('/var/lib/mozevents/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mozevents.settings' 

import django.core.handlers.wsgi 

application = django.core.handlers.wsgi.WSGIHandler()
