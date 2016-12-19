from django.contrib import admin
from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportModelAdmin


Category = apps.get_registered_model('mrejesho', 'Category')
Feedback = apps.get_registered_model('mrejesho', 'Feedback')


class CategoryAdmin(ImportExportModelAdmin):
    readonly_fields = ['id', 'date_created', 'date_updated']


class FeedbackAdmin(ImportExportModelAdmin):
    readonly_fields = ['id', 'date_created', 'date_updated',
                      'sender_name', 'sender_email', 'sender_phone',
                      'sender_organization', 'message']
    filter_horizontal = ['category']
    list_display = ['id', 'sender_name', 'message', 'status', 'remarks']
    list_display_links = ['id', 'sender_name']
    search_fields = ['sender_name', '=id', 'message']
    list_filter = ['category', 'status']
    fieldsets = (
        (_('Sender'), {
           'fields': ('sender_name', 'sender_email', 'sender_phone',
                      'sender_organization')
        }),
        (_('Feedback'), {
           'fields': ('message', 'id', 'date_created', 'date_updated')
        }),
        (_('Internal'), {
            'fields': ( 'status', 'remarks', 'category',
                       'notified_staff'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'date_created', 'date_updated',
                    'sender_name', 'sender_email', 'sender_phone',
                    'sender_organization', 'message']
        else:
            return ['id', 'date_created', 'date_updated']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
