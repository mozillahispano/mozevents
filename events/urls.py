from django.conf.urls import patterns, url


urlpatterns = patterns('events.views',
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/confirm/(?P<hash>\w+)$',
        'confirmation'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/decline/(?P<hash>\w+)$',
        'decline'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/registration/$', 'registration'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/tweets/$', 'tweets'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', 'detail'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/events/category/$', 'events_category'),
	url(r'^filter_events/$', 'filter_events'),
)
