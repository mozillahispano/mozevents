# coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.views.generic.simple import direct_to_template
from django.template import RequestContext

# Templates in Django need a "Context" to parse with, so we'll borrow this.
# "Context"'s are really nothing more than a generic dict wrapped up in a
# neat little function call.
from django.template import Context

from events.models import Event, Registration
from events.forms import RegistrationForm

# l10n
from django.utils.translation import ugettext_lazy as _

# Magic funtions to handle some unicode strings
from django.utils.encoding import smart_str, smart_unicode

# For random hashes
import uuid

from events.utils import newMail

def index(request):
        
        eventList = Event.objects.filter(active=True).order_by('-eventDate')
        
        data = {
            'events': eventList,
        }
	
	return render_to_response('index.html', data, context_instance=RequestContext(request))
        
def detail(request, id, slug):
        
        event = get_object_or_404(Event, id=id, active=True)
        
        data = {
            'event': event,
        }
	
	return render_to_response('events/detail.html', data, context_instance=RequestContext(request))
        
def registration(request, id, slug):
        
        event = get_object_or_404(Event, id=id, active=True)
        
        data = {
                    'event': event,
        }
        
        # If registration is closed, we should display a different page
	if event.registrationOpen is False:
		return render_to_response("events/registration-closed.html", data)
                
        if request.method == "POST":
            
            form = RegistrationForm(request.POST, request.FILES)
            
            if form.is_valid():
                
                registration = form.save(commit=False)
                registration.event = event
                registration.confirmed = False
                registration.hash = uuid.uuid1().hex
                registration.name = smart_str(registration.firstName) + " " + smart_str(registration.familyName)
                registration.save()
                
                #Email confirmation
                newMail(event.id, registration.id)
		
		data = {
			'event': event,
			'form': form,
			'registration': registration,
                }
                
                return render_to_response('events/registration-done.html', data, context_instance=RequestContext(request))
                
            else:
		
		data = {
                    'event': event,
                    'form': form,
		}
                
                return render_to_response('events/registration.html', data, context_instance=RequestContext(request))
                
        else:
            
            form=RegistrationForm(instance = event)
            
            data = {
                    'event': event,
                    'form': form,
            }
            
            return render_to_response('events/registration.html', data, context_instance=RequestContext(request))
	    
def confirmation(request, id, slug, hash):
        
	event = get_object_or_404(Event, pk=id, active=True)
        registration = get_object_or_404(Registration, hash=hash)
	alreadyConfirmed = False
	
	# If already confirmed
	if registration.confirmed is True:
		alreadyConfirmed = True
	else:
		registration.confirmed = True
		registration.save()
        
        data = {
            'registration': registration,
	    'event': event,
	    'alreadyConfirmed': alreadyConfirmed,
        }
	
	return render_to_response('events/registration-confirmed.html', data, context_instance=RequestContext(request))