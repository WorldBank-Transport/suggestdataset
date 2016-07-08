from modeltranslation.translator import translator, TranslationOptions
from django.apps import apps


Category = apps.get_registered_model('datasets', 'Category')
Organization = apps.get_registered_model('datasets', 'Organization')
Dataset = apps.get_registered_model('datasets', 'Dataset')


class CommonTranslationOptions(TranslationOptions):
    fields = ['name', 'description']


translator.register(Category, CommonTranslationOptions)
translator.register(Organization, CommonTranslationOptions)
translator.register(Dataset, CommonTranslationOptions)
