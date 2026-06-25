"""
Cuadra Erre — Testing Settings
Configuración para pytest / CI.
Activa con: ENVIRONMENT=testing
"""

from .base import *  # noqa: F401,F403

DEBUG = False

ALLOWED_HOSTS = ['*']

# SQLite en memoria para tests rápidos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Deshabilitar throttling en tests
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []  # noqa: F405
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {}  # noqa: F405

# Hashing rápido en tests (bcrypt es lento por diseño)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Email en memoria
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
