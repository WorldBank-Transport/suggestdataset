from django.conf import settings


def site(request):
    return {
        'DEBUG': getattr(settings, 'DEBUG', False),
        'SITE_NAME': getattr(settings, 'SITE_NAME', ''),
        'SITE_URL': getattr(settings, 'SITE_URL', ''),
    }
