from django.conf.urls import *

from django.contrib import admin

admin.autodiscover()

# Importamos los los URLconf de nuestas apps
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'events.views.index'),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += patterns('events.views',
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/confirm/(?P<hash>\w+)$', 'confirmation'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/decline/(?P<hash>\w+)$', 'decline'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/$', 'registration'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/tweets/$', 'tweets'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'detail'),
)