# coding=utf-8
# This file contains some extra functions
import datetime
import string
import hashlib

from django.core.mail import send_mail
# Emails using templates
from django.template.loader import get_template
from django.template import Context

from django.conf import settings

from events.models import Event, Registration

# l10n
from django.utils.translation import ugettext_lazy as _

# Special functions for unicode strings
from django.utils.encoding import smart_str, smart_unicode

def newMail(event, registration):
	'''
            Send an email using a template
	'''
	event = Event.objects.get(pk=event)
			
	reg = Registration.objects.get(pk=registration)
	
	mailSubject = _("[%(name)s] Registration confirmation") % {'name': event.name}
			
	send_mail(
		mailSubject,
			get_template('events/registration-email.html').render(
				Context({
					'event': event,
					'reg': reg,
					'SITE_URL': settings.SITE_URL,
				})
			),
			settings.EMAIL_FROM,
			[reg.email],
			fail_silently = True
	)

def pendingMail(event, registration):
	'''
            Send an email noticing that you get a place from the queue
	'''
	event = Event.objects.get(pk=event)
			
	reg = Registration.objects.get(pk=registration)
	
	mailSubject = _("[%(name)s] You got a place!") % {'name': event.name}
			
	send_mail(
		mailSubject,
			get_template('events/registration-pendingEmail.html').render(
				Context({
					'event': event,
					'reg': reg,
					'SITE_URL': settings.SITE_URL,
				})
			),
			settings.EMAIL_FROM,
			[reg.email],
			fail_silently = True
	)