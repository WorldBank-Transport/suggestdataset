from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    """A Category."""
    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Desciption'), blank=True)
    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True)
    date_updated = models.DateTimeField(
        _('Date updated'), blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Organization(models.Model):
    """An Organization."""
    name = models.CharField(_('Organization name'), max_length=128)
    description = models.TextField(_('Desciption'), blank=True)
    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True)
    date_updated = models.DateTimeField(
        _('Date updated'), blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Dataset(models.Model):
    """A Dataset."""
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Desciption'), blank=True)
    likes = models.PositiveIntegerField(_('likes'), default=0,
                                        blank=True, null=True)
    categories = models.ManyToManyField(
        'datasets.Category', blank=True,
        verbose_name=_('Category'))
    organization = models.ForeignKey(
        'datasets.Organization', blank=True, null=True,
        verbose_name=_('Organization'))
    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True)
    date_updated = models.DateTimeField(
        _('Date updated'), blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = _("Dataset")
        verbose_name_plural = _("Datasets")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dataset-detail', args=[self.id])
