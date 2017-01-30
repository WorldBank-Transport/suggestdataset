from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField

from .models import Dataset


class DatasetSuggestForm(forms.ModelForm):

    suggester_name = forms.CharField(label=_('Your name'),
                                     required=True)
    suggester_email = forms.EmailField(label=_('Your email'),
                                       required=True)
    captcha = CaptchaField()

    class Meta:
        model = Dataset
        fields = [
            'suggester_name', 'suggester_email', 'name', 'categories',
            'description']
        labels = {
            'description': _('Description'),
            'categories': _('Category of the dataset')
        }
