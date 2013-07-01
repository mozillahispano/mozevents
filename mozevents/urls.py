from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'events.views.index', name='home'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^stats/', 'events.views.stats'),
)

# Our apps URLconfs
urlpatterns += patterns('events.views',
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/confirm/(?P<hash>\w+)$', 'confirmation'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/decline/(?P<hash>\w+)$', 'decline'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/$', 'registration'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/tweets/$', 'tweets'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'detail'),
)

urlpatterns += staticfiles_urlpatterns()
