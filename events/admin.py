# coding=utf-8
from django.contrib import admin

from events.models import Event, Registration

# l10n
from django.utils.translation import ugettext_lazy as _
    
class EventAdmin(admin.ModelAdmin):
    # Autofill slugs
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'eventDate', 'regStartDate', 'regEndDate', 'active')
    list_filter = ['active', 'regStartDate', 'country']
    search_fields = ['name']

    # TinyMCE
    class Media:
	js = ('/static/js/tiny_mce/tiny_mce.js', '/static/js/textareas.js')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website', 'event', 'creationDate', "volunteer", "press", 'confirmed')
    list_filter = ['event', 'confirmed', 'press', 'volunteer', 'creationDate']
    search_fields = ['name']
    

admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegistrationAdmin)

