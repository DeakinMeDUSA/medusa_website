import logging
import os
# noinspection PyUnresolvedReferences
import sys
# noinspection PyUnresolvedReferences
from pathlib import Path

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
logger = logging.getLogger(__name__)
# noinspection PyUnresolvedReferences
import medusa_website.mcq_bank.models
from medusa_website.users.models import User
# noinspection PyUnresolvedReferences
from rich import inspect
from rich.console import Console
# noinspection PyUnresolvedReferences
from django.conf import settings

user = User.objects.get(id=1)
console = Console()
print("Django initialised")
