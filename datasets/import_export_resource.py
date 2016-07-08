from django.apps import apps
from import_export import resources, fields, widgets


Category = apps.get_registered_model('datasets', 'Category')
Organization = apps.get_registered_model('datasets', 'Organization')
Dataset = apps.get_registered_model('datasets', 'Dataset')


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category


class OrganizationResource(resources.ModelResource):

    class Meta:
        model = Organization


class DatasetResource(resources.ModelResource):

    class Meta:
        model = Dataset
