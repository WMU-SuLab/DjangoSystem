"""
ASGI config for ManagementSystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"))
env = os.environ.get('DJANGO_ENV', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'Config.settings.{env}')

application = get_asgi_application()
