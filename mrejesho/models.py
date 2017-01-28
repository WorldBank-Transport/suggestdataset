from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from phonenumber_field.modelfields import PhoneNumberField


@python_2_unicode_compatible
class Category(models.Model):
    """Feedback Category."""
    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Desciption'), blank=True)
    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True)
    date_updated = models.DateTimeField(
        _('Date updated'), blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Feedback(models.Model):
    """Feedback."""
    RECEIVED = 'received'
    UNDER_REVIEW = 'under review'
    RESPONSE_SENT = 'response sent'
    STATUSES =(
        (RECEIVED, _('Received/Read')),
        (UNDER_REVIEW, _('Under review')),
        (RESPONSE_SENT, _('Response sent'))
    )

    sender_name = models.CharField(_('Name'), max_length=128)
    sender_email = models.EmailField(_('Email'), max_length=128,
                                     blank=True)
    sender_phone = PhoneNumberField(_('Phone'), blank=True)
    sender_organization = models.CharField(_('Organization'),
                                           max_length=128,
                                           blank=True)
    message = models.TextField(_('Message'))
    status = models.CharField(_('Status'), max_length=128,
                              choices=STATUSES, blank=True)
    category = models.ManyToManyField('mrejesho.Category', blank=True,
                                      related_name='feedbacks',
                                      verbose_name=_('Category'))
    remarks = models.TextField(_('Remarks'), blank=True)
    notified_staff = models.TextField(_('Notified staff'), blank=True)
    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True)
    date_updated = models.DateTimeField(
        _('Date updated'), blank=True, null=True, auto_now=True)


    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedback")
        permissions = (
            ('can_receive_new_feedback_email',
            _('Can receive notification on new feedback')),
        )

    def __str__(self):
        return self.message
