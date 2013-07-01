from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase

from nose.tools import eq_
from pyquery import PyQuery

from events.models import Event


class EventsIndexTests(TestCase):
    def test_events_index(self):
        """Verify that the proper events are listed."""
        url = reverse('home')

        # There should be no coming or past events yet.
        response = self.client.get(url)
        eq_(200, response.status_code)
        doc = PyQuery(response.content)
        eq_(0, len(doc('table.coming-events, table.past-events')))

        # Create a coming and a past event.
        Event.objects.create(
            name='Mozilla Hispano Work Week',
            slug='mozilla-hispano-work-week',
            eventDate=datetime.now() + timedelta(days=1),
            regStartDate=datetime.now() - timedelta(days=2),
            regEndDate=datetime.now() + timedelta(days=1),
            country='PR',
            city='Humacao',
            active=True)
        Event.objects.create(
            name='Mozilla Canada Work Week',
            slug='mozilla-canada-work-week',
            eventDate=datetime.now() - timedelta(days=1),
            regStartDate=datetime.now() - timedelta(days=2),
            regEndDate=datetime.now() - timedelta(days=1),
            country='CA',
            city='Toronto',
            active=True)

        # Verify there is 1 coming and 1 past event.
        response = self.client.get(url)
        eq_(200, response.status_code)
        doc = PyQuery(response.content)

        eq_(1, len(doc('table.coming-events tbody tr')))
        eq_(1, len(doc('table.past-events tbody tr')))
        assert 'Mozilla Hispano' in doc('table.coming-events').text()
        assert 'Mozilla Canada'in doc('table.past-events').text()
