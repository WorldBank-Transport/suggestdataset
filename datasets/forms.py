from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Dataset


class DatasetSuggestForm(forms.ModelForm):

    suggester_name = forms.CharField(label=_('Your full name'),
                                     required=True)
    suggester_email = forms.EmailField(label=_('Your email'),
                                       required=True)

    class Meta:
        model = Dataset
        fields = [
            'suggester_name', 'suggester_email',
            'suggester_organization', 'name', 'description']
        labels = {
            'suggester_organization': _('Your organization'),
            'description': _('Description')
        }
