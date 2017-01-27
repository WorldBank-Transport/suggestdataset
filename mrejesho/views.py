from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.apps import apps
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.db.models import Q
from .forms import FeedbackForm

Feedback = apps.get_registered_model('mrejesho', 'Feedback')
User = get_user_model()

DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')
EMAIL_FAIL_SILENTLY = getattr(settings, 'EMAIL_FAIL_SILENTLY', True)


class FeedbackCreate(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'mrejesho/feedback.html'

    def get_success_url(self):
        return reverse('feedback-thanks')

    def form_valid(self, form):
        self.object = form.save()
        site = get_current_site(self.request)
        email_ctx = {
            'site_name': site.name,
            'site_domain': site.domain,
            'feedback': self.object
        }
        self.notify_sender(email_ctx, site)
        self.notify_staff(email_ctx, site)
        return HttpResponseRedirect(self.get_success_url())

    def notify_sender(self, email_ctx, site):
        if self.object.sender_email:
            delivered_message = render_to_string(
                'mrejesho/emails/feedback_received.html', email_ctx)
            delivered_mail = EmailMessage(
                _('%(site_name)s: Feedback' %{'site_name': site.name}),
                delivered_message,
                DEFAULT_FROM_EMAIL,
                [self.object.sender_email]
            )
            delivered_mail.send(fail_silently=EMAIL_FAIL_SILENTLY)

    def notify_staff(self, email_ctx, site):
        perm = Permission.objects.get(
            codename='can_receive_new_feedback_email')
        notifiable_emails = User.objects.filter(
            Q(groups__permissions=perm) | Q(user_permissions=perm)
            ).distinct().values_list('email', flat=True)
        notifiable_emails = list(filter(None, notifiable_emails))
        if notifiable_emails:
            notification_message = render_to_string(
                'mrejesho/emails/new_feedback_received.html', email_ctx)
            notification_mail = EmailMessage(
                _('%(site_name)s: New Feedback received #%(feedback_id)s'
                %{'site_name': site.name, 'feedback_id': self.object.id}
                ),
                notification_message,
                DEFAULT_FROM_EMAIL,
                notifiable_emails
            )
            notification_mail.send(fail_silently=EMAIL_FAIL_SILENTLY)


class FeedbackThanks(TemplateView):
    template_name = 'mrejesho/feedback_thanks.html'
