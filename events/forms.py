# coding=utf-8
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str, smart_unicode

from events.models import Event, Registration
from events.extra import ReCaptchaField

class RegistrationForm(ModelForm):
	class Meta:
		model = Registration
		# We should exclude event field, we'll fill it depending
                # on the event
		exclude = ('event', 'status')
		
	# Non DB fields
	
	emailConfirm = forms.EmailField(label=_("Confirm email address"), max_length=100)
	recaptcha = ReCaptchaField(help_text=_("To avoid automatical registrations, you have to fill this field with the two words above. If you arent able to read them, you can reload a different ones from the arrows icon."))
	privacyPolicy = forms.BooleanField(label=_("I accept the privacy policy"), help_text=_("All your data will be incorporated to a database and will be used to organice and control the event assistants and contact you with information relevant to this event. We will not share your information with anyone and we will delete all data once the event is over unless you specify the opposite on the form to get information about Mozilla.<br />If you have any doubt or you want to correct or delete your information anytime, contacting us via email at eventos at mozilla-hispano.org"))
	
	# Validation rules
	
	def clean(self):
		# Recover fields with special validations
		cleaned_data = self.cleaned_data
		

		email = cleaned_data.get("email")
		emailConfirm = cleaned_data.get("emailConfirm")

		if email != emailConfirm:
			msg = _("The email doesn't match")
			self._errors["emailConfirm"] = self.error_class([msg])
                        
		return cleaned_data