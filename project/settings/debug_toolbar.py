from .installed_apps import INSTALLED_APPS
from .middleware import MIDDLEWARE
import os


DJANGO_DEBUG_TOOLBAR = 1 if os.environ.get('DJANGO_DEBUG_TOOLBAR') == '1' else 0 # noqa E501

if DJANGO_DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
