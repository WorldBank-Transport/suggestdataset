from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.apps import apps
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from django_filters.views import FilterView

from .filters import DatasetFilter


Category = apps.get_registered_model('datasets', 'Category')
Organization = apps.get_registered_model('datasets', 'Organization')
Dataset = apps.get_registered_model('datasets', 'Dataset')


class DatasetList(FilterView):
    queryset = Dataset.objects\
        .prefetch_related('categories', 'organization')\
        .order_by('-date_created')
    template_name = 'datasets/dataset_list.html'
    context_object_name = 'datasets'
    filterset_class = DatasetFilter

    def get_context_data(self, **kwargs):
        ctx = super(DatasetList, self).get_context_data(**kwargs)
        ctx['categories'] = Category.objects.values()
        ctx['organizations'] = Organization.objects.values()
        return ctx



class DatasetDetail(DetailView):
    model = Dataset
    template_name = 'datasets/dataset_detail.html'
    context_object_name = 'dataset'


class DatasetLikeCreate(UpdateView):
    model = Dataset
    fields = ['id']

    @method_decorator(require_http_methods(["POST"]))
    def dispatch(self, *args, **kwargs):
        return super(DatasetLikeCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        liked_datasets = self.request.session.get('liked_datasets')
        if not type(liked_datasets) is list:
            liked_datasets = []
        if form.instance.id in liked_datasets:
            print 'Already liked'
            messages.info(
                self.request,
                _('Thanks, we already received your suggestion: '
                '<a href="%s" class="alert-link">%s</a>'
                %(form.instance.get_absolute_url(), form.instance.name)))
        else:
            form.instance.likes += 1
            form.save()
            liked_datasets.append(form.instance.id)
            self.request.session['liked_datasets'] = liked_datasets
            messages.info(
                self.request,
                _('Thanks for your suggestion: <a class="alert-link"'
                'href="%s">%s</a>'
                %(form.instance.get_absolute_url(), form.instance.name)))
        return super(DatasetLikeCreate, self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse(self.object)
        return next_url
