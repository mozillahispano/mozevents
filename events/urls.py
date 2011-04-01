from django.conf.urls.defaults import *

urlpatterns = patterns('events.views',
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/confirm/(?P<hash>\w+)$', 'confirmation'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/$', 'registration'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'detail'),
)