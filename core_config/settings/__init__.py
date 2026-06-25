# core_config/settings/__init__.py
# Importa los settings según el entorno.
# Por defecto usa development. En producción, configura:
#   DJANGO_SETTINGS_MODULE=core_config.settings.production

import os

env = os.getenv('ENVIRONMENT', 'development').lower()

if env == 'production':
    from .production import *
elif env == 'testing':
    from .testing import *
else:
    from .development import *
