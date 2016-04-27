# coding=utf-8
import datetime
import uuid

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str, smart_unicode
from django.views.generic import TemplateView

from events.forms import RegistrationForm, FilterEventSearch
from events.models import Event, Registration, Category
from events.utils import newMail, pendingMail


def index(request):
    """Events index (home) page."""
    now = datetime.datetime.now()

    nextEvents = Event.objects.filter(
        active=True, eventDate__gte=now).order_by('eventDate')
    oldEvents = Event.objects.filter(
        active=True, eventDate__lt=now).order_by('-eventDate')

    categories = Category.objects.all()

    formFilter = FilterEventSearch()

    data = {
        'nextEvents': nextEvents,
        'oldEvents': oldEvents,
        'categories': categories, 
        'formFilter': formFilter,   
    }

    return render_to_response(
        'index.html', data, context_instance=RequestContext(request))

def detail(request, id, slug):
    """Event details page."""
    event = get_object_or_404(Event, id=id, active=True)

    data = {
        'event': event
    }

    return render_to_response(
        'events/detail.html', data, context_instance=RequestContext(request))


def registration(request, id, slug):
    """Event registrations page."""
    event = get_object_or_404(Event, id=id, active=True)

    # If registration is closed, we should display a different page
    if event.registrationOpen is False:
        return render_to_response(
            "events/registration-closed.html", {'event': event})

    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.status = "Invited"
            registration.hash = uuid.uuid1().hex
            registration.name = '%s %s' % (
                smart_str(registration.firstName),
                smart_str(registration.familyName))

            registration.save()

            # Email confirmation
            newMail(event.id, registration.id)

            data = {
                'event': event,
                'form': form,
                'registration': registration,
            }

            return render_to_response(
                'events/registration-done.html',
                data,
                context_instance=RequestContext(request))

    else:
        form = RegistrationForm(instance=event)

    return render_to_response(
        'events/registration.html',
        {'event': event, 'form': form},
        context_instance=RequestContext(request))


def confirmation(request, id, slug, hash):
    """
    Handle links sent to email to confirm registration
    and set proper status for the record.
    """
    event = get_object_or_404(Event, pk=id, active=True)
    registration = get_object_or_404(Registration, hash=hash)

    alreadyConfirmed = False

    # placesLeft will change if confirmed, so we need a flag
    inQueue = False

    # If already confirmed
    if registration.status == "Confirmed":
        alreadyConfirmed = True
    elif event.queueActive:
        if event.placesLeft < 1:
            # If it's a record that was on queue and got a place
            if registration.status == "Pending":
                registration.status = "Confirmed"
            else:
                registration.status = "Queued"
                inQueue = True
        else:
            registration.status = "Confirmed"
    else:
        registration.status = "Confirmed"

    registration.save()

    data = {
        'registration': registration,
        'event': event,
        'alreadyConfirmed': alreadyConfirmed,
        'inQueue': inQueue,
    }

    if registration.status == "Confirmed":
        return render_to_response(
            'events/registration-confirmed.html',
            data,
            context_instance=RequestContext(request))

    return render_to_response(
        'events/registration-queued.html',
        data,
        context_instance=RequestContext(request))


def decline(request, id, slug, hash):
    """
    Handle links sent to email to decline registration
    and set proper status for the record.
    """
    event = get_object_or_404(Event, pk=id, active=True)
    registration = get_object_or_404(Registration, hash=hash)

    prevStatus = registration.status
    registration.status = "Declined"
    registration.save()

    # We release a place for the next one in queue and send him and email
    # but only if his previous status was Confirmed or Pending
    # FIXME: I'm sure there is a better way to do this
    if (event.queueActive and prevStatus == "Confirmed" or
        prevStatus == "Pending"):

        nextInQueueId = Registration.objects.filter(
            event=event.id, status="Queued").order_by('creationDate')[:1]

        if nextInQueueId:
            nextInQueue = Registration.objects.get(pk=nextInQueueId[0].id)
            nextInQueue.status = "Pending"
            nextInQueue.save()
            # Email confirmation
            pendingMail(event.id, nextInQueue.id)

    data = {
        'registration': registration,
        'event': event
    }

    return render_to_response(
        'events/registration-declined.html',
        data,
        context_instance=RequestContext(request))


def tweets(request, id, slug):
    """Event tweets page."""
    event = get_object_or_404(Event, id=id, active=True)

    return render_to_response(
        'events/tweets.html',
        {'event': event},
        context_instance=RequestContext(request))


@login_required
def stats(request):
    """Global stats page."""
    eventList = Event.objects.filter(active=True).order_by('eventDate')
    registrations = Registration.objects

    eventNo = eventList.count()
    registered = registrations.count()
    regAvg = registered / eventNo
    attended = registrations.filter(status='Attended').count()

    if registered > 0:
        gSuccessRatio = round(float(attended) / float(registered)*100, 2)
    else:
        gSuccessRatio = 0

    data = {
        'events': eventList,
        'registrations' : registrations,
        'eventNo' : eventNo,
        'registered' : registered,
        'regAvg' : regAvg,
        'attended' : attended,
        'gSuccessRatio' : gSuccessRatio,
    }

    return render_to_response(
        'stats/index.html', data, context_instance=RequestContext(request))

def events_category(request, id, slug):
    """
        Filter evets for category
    """
    try:
        events = Event.objects.filter(category_id=id)
    except Event.DoesNotExist:
        raise Http404(_("Selected category nonexistent"))
    
    category = get_object_or_404(Category, id=id)

    data = {
        'events': events,
        'category': category,
    }

    return render_to_response(
        'events/events_categories.html', data, context_instance=RequestContext(request))

def filter_events(request):

    """
        Results of the filters of events
    """

    try:
        country = request.POST.get('country')
        category = request.POST.get('category')
        keyword = request.POST.get('keyword')
        eventDateFrom = request.POST.get('eventDateFrom')
        eventDateTo = request.POST.get('eventDateTo')
        
        if (not country and not category and not keyword
            and not eventDateFrom and not eventDateTo):
            return HttpResponseRedirect("/")

        kwargs = {}

        if country:
            kwargs['country'] = country

        if category:
            kwargs['category'] = category

        if keyword:
            kwargs['name__icontains'] = keyword

        if eventDateFrom:
            eventDateFrom = datetime.datetime.strptime(
                            eventDateFrom, "%d/%m/%Y").strftime("%Y-%m-%d")

            kwargs['eventDate__gte'] = eventDateFrom

        if eventDateTo:
            eventDateTo = datetime.datetime.strptime(
                            eventDateTo, "%d/%m/%Y").strftime("%Y-%m-%d")

            kwargs['eventDate__lte'] = eventDateTo

        events = Event.objects.filter(**kwargs).order_by("-eventDate")

        data = {
            'events': events,
        }

        return render_to_response(
            'events/filter_events.html', data, context_instance=RequestContext(request))
         
    except Exception, e:
        raise Http404(_("Failed the filter"))


