# coding=utf-8
from django.db import models
from django.forms import ModelForm

import datetime

# l10n
from django.utils.translation import ugettext_lazy as _

# Models

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
    address = models.CharField(_("Address"), max_length=200, help_text=_("The address should be searchable in Google Maps"))
    places = models.IntegerField(_("Places"), blank=True, null=True, help_text=_("Number of places, leave blank for unlimited"))
    description = models.TextField(_("Event description and program"), blank=True, null=True)
    commentsUrl = models.CharField(_("Comments url"), max_length=200, help_text=_("Link to comments at the forum"))
    active = models.BooleanField(_("Active"))
    twitterTag = models.CharField(_("Social tag"), max_length=50, help_text=_("Tag for this event at Twitter and Flickr, e.g fx4madrid. Note: Do not add # to the tag, it will be added auto for Twitter."))
    
    def registrationOpen(self):
        '''
            Returns if incriptions are open.
        '''
        now = datetime.datetime.now()
        if now >= self.regStartDate and now <= self.regEndDate:
            return True
        else:
            return False
                    
    registrationOpen = property(registrationOpen)
                
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
    website = models.URLField(_("Website"), max_length=200, blank=True, null=True)
    confirmed = models.BooleanField(_("Confirmed"))
    
    hash = models.CharField(max_length=200, editable=False)
    
    def __unicode__(self):
        return self.name
