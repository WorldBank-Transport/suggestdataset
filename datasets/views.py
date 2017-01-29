from django.conf import settings
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.apps import apps
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from django_filters.views import FilterView

from .filters import DatasetFilter, DatasetLikingFilter
from .forms import DatasetSuggestForm


Category = apps.get_registered_model('datasets', 'Category')
Organization = apps.get_registered_model('datasets', 'Organization')
Dataset = apps.get_registered_model('datasets', 'Dataset')
User = get_user_model()

DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')
EMAIL_FAIL_SILENTLY = getattr(settings, 'EMAIL_FAIL_SILENTLY', True)


class DatasetSuggestions(FilterView):
    queryset = Dataset.objects.filter(archived=False, is_public=True)
    template_name = 'datasets/dataset_suggestions.html'
    context_object_name = 'datasets'
    filterset_class = DatasetFilter

    def get_context_data(self, **kwargs):
        ctx = super(DatasetSuggestions, self).get_context_data(**kwargs)
        ctx['categories'] = Category.objects.values()
        ctx['organizations'] = Organization.objects.values()
        ctx['suggest_form'] = DatasetSuggestForm()
        return ctx


class DatasetDetail(DetailView):
    queryset = Dataset.objects.filter(archived=False, is_public=True)
    template_name = 'datasets/dataset_detail.html'
    context_object_name = 'dataset'


class DatasetLikeCreate(UpdateView):
    queryset = Dataset.objects.filter(archived=False, is_public=True)
    fields = ['id']

    @method_decorator(require_http_methods(["POST"]))
    def dispatch(self, *args, **kwargs):
        if not self.request.META.get('HTTP_USER_AGENT', None):
            return HttpResponseForbidden()
        return super(DatasetLikeCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        liked_datasets = self.request.session.get('liked_datasets')
        if not type(liked_datasets) is list:
            liked_datasets = []
        if form.instance.id in liked_datasets:
            messages.info(
                self.request,
                _("Thanks, we already received your 'vote': "
                "<a href='%s' class='alert-link'>%s</a>"
                %(form.instance.get_absolute_url(), form.instance.name)))
        else:
            form.instance.likes += 1
            form.save()
            liked_datasets.append(form.instance.id)
            self.request.session['liked_datasets'] = liked_datasets
            messages.info(
                self.request,
                _('Thanks for your vote: <a class="alert-link"'
                'href="%s">%s</a>'
                %(form.instance.get_absolute_url(), form.instance.name)))
        return super(DatasetLikeCreate, self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse(self.object)
        return next_url


class DatasetSuggest(CreateView):
    model = Dataset
    form_class = DatasetSuggestForm
    template_name = 'datasets/dataset_suggest.html'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request,
                         _('Thanks, we have received your suggestion:'
                         '"%(dataset_name)s"'
                         %{'dataset_name': self.object.name}))

        site = get_current_site(self.request)
        email_ctx = {
            'site_name': site.name,
            'site_domain': site.domain,
            'dataset': self.object
        }
        self.notify_sender(email_ctx, site)
        self.notify_staff(email_ctx, site)
        return HttpResponseRedirect(self.get_success_url())

    def notify_sender(self, email_ctx, site):
        if self.object.suggester_email:
            delivered_message = render_to_string(
                'datasets/emails/suggestion_received.html', email_ctx)
            delivered_mail = EmailMessage(
                _('%(site_name)s: Dataset Suggestion'
                %{'site_name': site.name}),
                delivered_message,
                DEFAULT_FROM_EMAIL,
                [self.object.suggester_email]
            )
            delivered_mail.send(fail_silently=EMAIL_FAIL_SILENTLY)

    def notify_staff(self, email_ctx, site):
        perm = Permission.objects.get(
            codename='can_receive_new_suggestion_email')
        notifiable_emails = User.objects.filter(
            Q(groups__permissions=perm) | Q(user_permissions=perm)
            ).distinct().values_list('email', flat=True)
        notifiable_emails = list(filter(None, notifiable_emails))
        if notifiable_emails:
            notification_message = render_to_string(
                'datasets/emails/new_suggestion_received.html',
                email_ctx)
            notification_mail = EmailMessage(
                _('%(site_name)s: New Dataset suggestion received'
                '#%(suggestion_id)s' %{'site_name': site.name,
                'suggestion_id': self.object.id}),
                notification_message,
                DEFAULT_FROM_EMAIL,
                notifiable_emails
            )
            notification_mail.send(fail_silently=EMAIL_FAIL_SILENTLY)

    def get_success_url(self):
        return reverse('dataset-suggestions')
