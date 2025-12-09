from django.conf import settings

def assistant_enabled(request):
    """Make ASSISTANT_ENABLED available in all templates."""
    return {
        'ASSISTANT_ENABLED': settings.ASSISTANT_ENABLED
    }
