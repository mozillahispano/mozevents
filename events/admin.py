# coding=utf-8
import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from events.models import Event, Registration
from events.utils import newMail, pendingMail

def export_as_csv_action(description=_("Export selected objects as CSV file"),
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset
        
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
        
        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode("utf-8") for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv


class RegistrationInline(admin.TabularInline):
    model = Registration
    list_display = ('name', 'email', 'website', 'event', 'twitter', 'volunteer', 'press', 'mailme', 'confirmed', 'attended', 'creationDate')
    list_filter = ['confirmed', 'press', 'volunteer', 'attended', 'mailme', 'creationDate', 'event']
    search_fields = ['name', 'email']
    
class EventAdmin(admin.ModelAdmin):
    # Autofill slugs
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'eventDate', 'regStartDate', 'regEndDate', 'active')
    list_filter = ['active', 'regStartDate', 'country']
    search_fields = ['name']
    
    inlines = [
	RegistrationInline,
    ]

    # TinyMCE
    class Media:
	js = ('/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js')
	
def reg_attended(modeladmin, request, queryset):
    queryset.update(status="Attended")
reg_attended.short_description = _("This registration has attended to the event")

def reg_confirmed(modeladmin, request, queryset):
    queryset.update(status="Confirmed")
reg_confirmed.short_description = _("Confirm manually place for this registration")

def reg_declined(modeladmin, request, queryset):
    queryset.update(status="Declined")
reg_declined.short_description = _("Decline manually this registration")

def reg_pending(modeladmin, request, queryset):
    queryset.update(status="Pending")
    
    for obj in queryset:
	pendingMail(obj.event.id, obj.id)
reg_pending.short_description = _("Set as pending and send an email to confirm")

def reg_privacy_clean(modeladmin, request, queryset):
    queryset.update(name="Deleted", firstName="Name", familyName="Deleted", email="Deleted")
reg_privacy_clean.short_description = _("[Privacy] Delete personal information")

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website', 'event', 'twitter', 'status', 'volunteer', 'press', 'mailme', 'creationDate')
    list_filter = ['status', 'press', 'volunteer', 'mailme', 'creationDate', 'event']
    search_fields = ['name', 'email']
    actions = [export_as_csv_action(_("Export selected registrations as CSV file"), fields=['id', 'name', 'email', 'website', 'twitter', 'volunteer', 'press'], header=True), reg_attended, reg_privacy_clean, reg_confirmed, reg_declined, reg_pending]
    

admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegistrationAdmin)

