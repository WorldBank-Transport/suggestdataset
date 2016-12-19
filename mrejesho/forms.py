from django import forms
from django.utils.translation import ugettext_lazy as _
from django.apps import apps

Feedback = apps.get_registered_model('mrejesho', 'Feedback')


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = [
            'sender_name', 'sender_email', 'sender_phone',
            'sender_organization', 'message']
        labels = {
            'sender_name': _('Your name'),
            'sender_email': _('Your email'),
            'sender_phone': _('Your phone'),
            'sender_organization': _('Your organization'),
            'message': _('Your message'),
        }

    def clean(self):
        data = self.cleaned_data
        if data.get('sender_email', None) or\
                data.get('sender_phone', None):
            return data
        else:
            raise forms.ValidationError(
                _('Please provide either a valid email address '
                  'or phone number'))
