from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

# Recaptcha stuff
import recaptcha.recaptcha as captcha

class ReCaptcha(forms.widgets.Widget):
    recaptcha_challenge_name = 'recaptcha_challenge_field'
    recaptcha_response_name = 'recaptcha_response_field'

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, True))

    def value_from_datadict(self, data, files, name):
        return [data.get(self.recaptcha_challenge_name, None), 
            data.get(self.recaptcha_response_name, None)]

class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('http://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.min.css',)
        }
        js = ('http://code.jquery.com/ui/1.11.4/jquery-ui.min.js',)