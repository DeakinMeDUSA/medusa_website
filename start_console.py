import os

import django
from rich.console import Console

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from medusa_website.users.models import User

user = User.objects.get(id=1)
console = Console()
print("Django initialised")
