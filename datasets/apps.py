from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DatasetsConfig(AppConfig):
    name = 'datasets'
    verbose_name = _('Datasets Suggestions')
