from django.conf import settings


def site(request):
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', ''),
    }
