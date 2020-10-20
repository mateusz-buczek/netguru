from .base import *  # noqa

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

THIRD_PARTY_APPS += ['debug_toolbar']

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ("127.0.0.1", "172.17.0.1")

try:
    from .local import *
except ImportError:
    pass
