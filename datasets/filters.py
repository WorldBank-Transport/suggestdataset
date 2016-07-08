from django.apps import apps

import django_filters

Dataset = apps.get_registered_model('datasets', 'Dataset')
Category = apps.get_registered_model('datasets', 'Category')


class DatasetFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(
        name='categories', queryset=Category.objects.all())

    class Meta:
        model = Dataset
        fields = ['categories', 'organization']
