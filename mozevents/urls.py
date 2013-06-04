from django.conf.urls import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'events.views.index'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^stats/', 'events.views.stats'),
)

# Our apps URLconfs
urlpatterns += patterns('events.views',
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/confirm/(?P<hash>\w+)$', 'confirmation'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/decline/(?P<hash>\w+)$', 'decline'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/$', 'registration'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/tweets/$', 'tweets'),
    (r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'detail'),
)

urlpatterns += staticfiles_urlpatterns()
