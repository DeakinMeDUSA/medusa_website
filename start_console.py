import logging
import os

import django

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from rich.console import Console

from medusa_website.users.models import User

logger = logging.getLogger(__name__)
user = User.objects.get(id=1)
console = Console()
print("Django initialised")
