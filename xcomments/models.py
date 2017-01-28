from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_comments.models import CommentAbstractModel
from django_comments.signals import comment_was_posted
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')
EMAIL_FAIL_SILENTLY = getattr(settings, 'EMAIL_FAIL_SILENTLY', True)


class XComment(CommentAbstractModel):

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        permissions = (
            ('can_receive_new_comment_email',
            _('Can receive notification on new comments')),
        )

def notify_sender(sender, comment, request, *args, **kwargs):

    site = get_current_site(request)
    email_ctx = {
        'site_name': site.name,
        'site_domain': site.domain,
        'comment': comment
    }

    if comment.user_email:
        site = get_current_site(request)
        delivered_message = render_to_string(
            'comments/emails/comment_received.html', email_ctx)
        delivered_mail = EmailMessage(
            _('%(site_name)s: Comment Received'
            %{'site_name': site.name}),
            delivered_message,
            DEFAULT_FROM_EMAIL,
            [comment.user_email]
        )
        delivered_mail.send(fail_silently=EMAIL_FAIL_SILENTLY)


def notify_staff(sender, comment, request, *args, **kwargs):
    site = get_current_site(request)
    User = get_user_model()
    email_ctx = {
        'site_name': site.name,
        'site_domain': site.domain,
        'comment': comment
    }
    perm = Permission.objects.get(
        codename='can_receive_new_comment_email')
    notifiable_emails = User.objects.filter(
        Q(groups__permissions=perm) | Q(user_permissions=perm)
        ).distinct().values_list('email', flat=True)
    notifiable_emails = list(filter(None, notifiable_emails))
    if notifiable_emails:
        notification_message = render_to_string(
            'comments/emails/new_comment_received.html', email_ctx)
        notification_mail = EmailMessage(
            _('%(site_name)s: New Comment received'
            '#%(comment_id)s' %{'site_name': site.name,
            'comment_id': comment.id}),
            notification_message,
            DEFAULT_FROM_EMAIL,
            notifiable_emails
        )
        notification_mail.send(fail_silently=EMAIL_FAIL_SILENTLY)

comment_was_posted.connect(notify_sender, sender=XComment)
comment_was_posted.connect(notify_staff, sender=XComment)
