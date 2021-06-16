import logging
import sys
from pathlib import Path
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
logger = logging.getLogger(__name__)
from medusa_website.mcq_bank.models import *
from medusa_website.users.models import User
from rich import inspect
from rich.console import Console
from django.urls import reverse
from django.conf import settings
user = User.objects.get(id=1)
console = Console()
print("Django initialised")