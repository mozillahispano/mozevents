# coding=utf-8
from django.contrib import admin

from events.models import Event, Registration

# l10n
from django.utils.translation import ugettext_lazy as _

# For cvs exportation
import csv
from django.http import HttpResponse

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

class EventAdmin(admin.ModelAdmin):
    # Autofill slugs
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'eventDate', 'regStartDate', 'regEndDate', 'active')
    list_filter = ['active', 'regStartDate', 'country']
    search_fields = ['name']

    # TinyMCE
    class Media:
	js = ('/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js')
	
def reg_attended(modeladmin, request, queryset):
    queryset.update(attended=True)
reg_attended.short_description = _("This registration has attended to the event")

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website', 'event', 'twitter', "volunteer", "press", 'confirmed', 'attended', 'creationDate')
    list_filter = ['event', 'confirmed', 'press', 'volunteer', 'attended', 'creationDate']
    search_fields = ['name', 'email']
    actions = [export_as_csv_action(_("Export selected registrations as CSV file"), fields=['id', 'name', 'email', 'website', 'twitter', 'volunteer', 'press'], header=True), reg_attended]
    

admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegistrationAdmin)

