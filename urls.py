from django.conf.urls.defaults import *

from django.contrib import admin

admin.autodiscover()

# Importamos los los URLconf de nuestas apps
urlpatterns = patterns('',
    (r'^event/', include('events.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'events.views.index'),
    (r'^i18n/', include('django.conf.urls.i18n')),
)