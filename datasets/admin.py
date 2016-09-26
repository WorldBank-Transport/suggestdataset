from django.contrib import admin
from django.apps import apps

from import_export.admin import ImportExportModelAdmin

from . import import_export_resource as resources


Category = apps.get_registered_model('datasets', 'Category')
Organization = apps.get_registered_model('datasets', 'Organization')
Dataset = apps.get_registered_model('datasets', 'Dataset')


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = resources.CategoryResource
    readonly_fields = ['id', 'date_created', 'date_updated']


class OrganizationAdmin(ImportExportModelAdmin):
    resource_class = resources.OrganizationResource
    readonly_fields = ['id', 'date_created', 'date_updated']


class DatasetAdmin(ImportExportModelAdmin):
    resource_class = resources.DatasetResource
    readonly_fields = ['id', 'date_created', 'date_updated', 'likes']
    filter_horizontal = ['categories']
    list_display = ['id', 'name', 'status', 'likes']
    list_display_links = ['id', 'name']
    list_select_related = ['organization']
    search_fields = ['name', '=id']
    list_filter = ['categories', 'status', 'organization', 'archived',
                   'date_created', 'date_updated']



admin.site.register(Category, CategoryAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Dataset, DatasetAdmin)
