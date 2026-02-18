from django.conf import settings

def assistant_enabled(request):
    """Make ASSISTANT_ENABLED available in all templates."""
    return {
        'ASSISTANT_ENABLED': settings.ASSISTANT_ENABLED
    }

def barrister_config(request):
    """
    Provides barrister-specific configuration to all templates.
    These values should be customized in core/settings.py for each deployment.
    """
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'David Nugent BL'),
        'BARRISTER_NAME': getattr(settings, 'BARRISTER_NAME', 'David Nugent'),
        'BARRISTER_EMAIL': getattr(settings, 'BARRISTER_EMAIL', 'david.nugent@lawlibrary.ie'),
        'BARRISTER_PHONE': getattr(settings, 'BARRISTER_PHONE', '01 291 6043'),
        'BARRISTER_MOBILE': getattr(settings, 'BARRISTER_MOBILE', ''),
        'CHAMBERS_ADDRESS_LINE1': getattr(settings, 'CHAMBERS_ADDRESS_LINE1', 'Law Library, Four Courts'),
        'CHAMBERS_ADDRESS_LINE2': getattr(settings, 'CHAMBERS_ADDRESS_LINE2', 'Dublin 7, Ireland'),
        'CHAMBERS_DX': getattr(settings, 'CHAMBERS_DX', ''),
        'YEAR_CALLED': getattr(settings, 'YEAR_CALLED', ''),
        'PRACTICE_AREAS_SHORT': getattr(settings, 'PRACTICE_AREAS_SHORT', 'Commercial/Chancery, Criminal, General Practice, Tort & Personal Injury'),
        'BARRISTER_BIO_FOOTER': getattr(settings, 'BARRISTER_BIO_FOOTER', 'Junior Counsel practising in Commercial/Chancery, Criminal, General Practice, and Tort & Personal Injury Law. Dublin, Eastern & Midland Circuits.'),
        'CIRCUITS': getattr(settings, 'CIRCUITS', 'Dublin, Eastern & Midland'),
        'QUALIFICATIONS': getattr(settings, 'QUALIFICATIONS', ''),
    }
