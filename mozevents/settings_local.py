from settings import *

# Change these settings to fit your needs

SITE_URL = "http://eventos.mozilla-hispano.org"
SITE_TITLE = "Mozilla Hispano"

EMAIL_FROM = 'eventos@mozilla-hispano.org'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = "587"
EMAIL_HOST_PASSWORD = 'EventosMh11'
EMAIL_HOST_USER = 'eventos@mozilla-hispano.org'
EMAIL_USE_TLS = True

# Recaptcha service keys
RECAPTCHA_PUBLIC_KEY = '6Le-B8MSAAAAAJ1K-dS6oVyoUHgYIFy8qrUac4Ky'
RECAPTCHA_PRIVATE_KEY = '6Le-B8MSAAAAAE59wTp4MyhIjEk07hMxR3sVloHx'

ADMINS = (
    ('Mozilla Events', 'eventos@mozilla-hispano.org'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mozevents',                      # Or path to database file if using sqlite3.
        'USER': 'mozevents',                      # Not used with sqlite3.
        'PASSWORD': 'bCaReK9LWTL5ER43',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'
