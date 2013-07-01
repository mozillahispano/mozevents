from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'events.views.index', name='home'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^stats/', 'events.views.stats'),
    url(r'^', include('events.urls')),
)

urlpatterns += staticfiles_urlpatterns()
