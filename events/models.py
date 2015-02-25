# coding=utf-8
import datetime

from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str, smart_unicode
from django.template import defaultfilters

from django_countries.countries import COUNTRIES

class Event(models.Model):
    '''
        Main event model
    '''
    
    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(_("Slug"))
    creationDate = models.DateTimeField(_("Creation date"), auto_now_add=True)
    eventDate = models.DateTimeField(_("Event date"))
    regStartDate = models.DateTimeField(_("Registration start date"))
    regEndDate = models.DateTimeField(_("Registration end date"))
    country = models.CharField(_("Country"), choices=COUNTRIES, max_length=2)
    city = models.CharField(_("City"), max_length=200)
    address = models.CharField(_("Address"), max_length=200, help_text=_("The address should be searchable in Google Maps"))
    places = models.IntegerField(_("Places"), blank=True, null=True, help_text=_("Number of places, leave blank for unlimited"))
    description = models.TextField(_("Event description and program"), blank=True, null=True)
    commentsUrl = models.CharField(_("Comments url"), max_length=200, help_text=_("Link to comments at the forum"), blank=True, null=True)
    active = models.BooleanField(_("Active"))
    twitterTag = models.CharField(_("Social tag"), max_length=50, help_text=_("Tag for this event at Twitter and Flickr, e.g fx4madrid. Note: Do not add # to the tag, it will be added auto for Twitter."))
    queueActive = models.BooleanField(_("Queue active"))
    queueSize = models.IntegerField(_("Queue max. size"), blank=True, null=True, help_text=_("Max. people on the queue, set 0 for no limit"))
    queueWaitTime = models.IntegerField(_("Max. time to answer queue (hours)"), blank=True, null=True, help_text=_("Max. time a person has to answer when he get a place for the event (in hours)"))
    
    def placesLeft(self):
        '''
            Returns how many places an event has left
        '''
        
        if self.places!=None:
            places = self.places - Registration.objects.filter(event=self.id, status="Confirmed").count()
            # If we add people manually to the event, we dont want to show a negative count ;)
            if places < 0:
                places = 0
            
            # If there are places left but any record is pending, no direct places should be offered
            # because they have to go to the queue if available
            if Registration.objects.filter(event=self.id, status="Pending").count():
                places = 0
        else:
            # TODO: Think of a better fix for events with unlimited (None) places
            return 'unlimited'

        return places
    
    placesLeft = property(placesLeft)
    
    def queueFull(self):
        '''
            Returns if the queue is full
        '''
        inQueue = Registration.objects.filter(event=self.id, status="Queued").count()
        
        # queueSize 0 is infinite
        if self.queueSize == 0:
            return False
        elif self.queueSize - inQueue < 1:
            return True
        else:
            return False
        
    queueFull = property(queueFull)
    
    def registrationOpen(self):
        '''
            Returns if incriptions are open.
        '''
        now = datetime.datetime.now()
        
        if now >= self.regStartDate and now <= self.regEndDate and self.placesLeft=='unlimited':
            return True
        # If we have places left
        elif now >= self.regStartDate and now <= self.regEndDate and self.placesLeft > 0:
            return True
        # If there is no places left but queue is not full
        elif now >= self.regStartDate and now <= self.regEndDate and self.placesLeft < 1 and self.queueActive and not self.queueFull:
            return True
        else:
            return False
                    
    registrationOpen = property(registrationOpen)
    
    def peopleAttended(self):
        '''
            Returns the number of people checked in as attended
        '''
        attended = Registration.objects.filter(event=self.id, status="Attended").count()
        
        return attended
    
    peopleAttended = property(peopleAttended)
    
    def __unicode__(self):
        return self.name

class Registration(models.Model):
    '''
        Model for individual registrations
    '''
    
    name = models.CharField(_("Name"), max_length=100, editable=False)
    firstName = models.CharField(_("First name"), max_length=30)
    familyName = models.CharField(_("Family name"), max_length=30)
    
    event = models.ForeignKey(Event)
    creationDate = models.DateTimeField(_("Creation date"), auto_now_add=True)
    email = models.EmailField(_("Email"), max_length=100)
    twitter = models.CharField(_("Twitter user"), max_length=100, blank=True, null=True)
    press = models.BooleanField(_("Press"), help_text=_("Check this field if you are you from press or other media"))
    volunteer = models.BooleanField(_("I want to help as a volunteer"), help_text=_("Check this field if you to want to help us at the event as a volunteer, we will contact you with more details"))
    website = models.URLField(_("Website"), max_length=200, blank=True, null=True)
    mailme = models.BooleanField(_("Keep my information after the event"), help_text=_("I allow Mozilla to contact me in the future with related information (about the community, next events...)"))
    
    '''
        Workflow:
            * You fill the form: Invited
            * You confirm the email: Confirmed
            * You confirm the email but place limit was reached: Queued
            * You get a spot from the queue and confirm: Confirmed
            * You get a spot from the queue and decline: Declined
            * You were in queue and you get a place to confirm: Pending
            * You get a spot from the queue and don't answer in time: Expired
            * You were confirmed and check-in on the event: Attended
    '''
    STATUS_CHOICES = (
        ('Invited', _("Invited")),
        ('Confirmed', _("Confirmed")),
        ('Declined', _("Declined")),
        ('Expired', _("Expired")),
        ('Queued', _("Queued")),
        ('Pending', _("Pending")),
        ('Attended', _("Attended"))
    )
    
    status = models.CharField(_("Status"), choices=STATUS_CHOICES, max_length=9, default="Invited")
    
    hash = models.CharField(max_length=200, editable=False)
    
    def save(self):
        # Updating the name field before saving
        self.name = smart_unicode(self.firstName) + " " + smart_unicode(self.familyName)
        super(Registration, self).save()
    
    def __unicode__(self):
        return self.name

class Category(models.Model):
    '''
        Model for categories of events
    '''

    id = models.AutoField(primary_key=True)
    name = models.CharField(_("Category"), max_length=100, default="")
    slug = models.SlugField(_("Slug"))
    description = models.TextField(_("Description"), blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class CategoryEvent(models.Model):
    '''
        Model for relationship between Event and Category
    '''

    event = models.ForeignKey(Event)
    category = models.ForeignKey(Category, verbose_name=_("Category"))