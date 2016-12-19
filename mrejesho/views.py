from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.apps import apps
from django.core.urlresolvers import reverse
from .forms import FeedbackForm

Feedback = apps.get_registered_model('mrejesho', 'Feedback')


class FeedbackCreate(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'mrejesho/feedback.html'

    def get_success_url(self):
        return reverse('feedback-thanks')


class FeedbackThanks(TemplateView):
    template_name = 'mrejesho/feedback_thanks.html'
