from django.conf import settings


def site_settings(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {
        'SITE_URL': settings.SITE_URL,
        'SITE_TITLE': settings.SITE_TITLE,
        'EMAIL_FROM': settings.EMAIL_FROM
    }
