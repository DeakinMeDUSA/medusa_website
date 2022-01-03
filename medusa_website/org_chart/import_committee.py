import datetime
import logging
import os
import sys
from pathlib import Path

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django

sys.path.append("I:/GitHub/medusa_website")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
logger = logging.getLogger(__name__)
from rich.console import Console

console = Console()

# %%
import random
import string

import pandas as pd
from django.conf import settings

from medusa_website.org_chart.models import (
    CommitteeMemberRecord,
    CommitteeRole,
    SubCommittee,
)
from medusa_website.users.models import MemberRecord, User
from medusa_website.utils.general import get_pretty_logger

df = pd.read_csv(Path(settings.ROOT_DIR / "backups/committee/committee_2022.csv"), dtype=str)


def get_random_letters(length=15):
    return "".join(random.choices(string.ascii_letters, k=length))


mems = []
for r in df.iterrows():
    mems.append(r[1])
logger = get_pretty_logger(__name__)
# %%
for m in mems:
    try:
        name = m.Name.strip()
        if not name or name == "nan" or name == "TBA":
            raise AttributeError()
    except AttributeError:
        logger.warning(f"IGNORING invalid row - {m}")
        continue
    logger.info(f"{'-' * 45}\nCreating/Updating CommitteeMemberRecord for {name}")
    try:
        try:
            user = User.objects.get(email=m["Medusa Member Email"])
            logger.info(f"Found existing user = {user}")
        except User.DoesNotExist:
            users = User.objects.filter(name__iexact=name).exclude(email__contains="medusa.org.au")
            if len(users) == 1:
                user = users[0]
                logger.info(f"Found existing user = {user}")
            elif len(users) > 1:
                logger.warning(f"Found MULTIPLE USERS : {users}")
                for i, _m in enumerate(users):
                    logger.warning(f"[{i}]  -  {_m.email} - {_m.name}")
                index = input("Enter index of which record to use:")
                user = users[int(index)]
            else:
                raise User.DoesNotExist()
    except User.DoesNotExist:
        try:
            try:
                mem_record = MemberRecord.objects.get(email=m["Medusa Member Email"])
            except MemberRecord.DoesNotExist:
                mem_records = MemberRecord.objects.filter(name__iexact=name).exclude(email__contains="medusa.org.au")
                if len(mem_records) == 1:
                    mem_record = mem_records[0]
                    logger.info(f"Found existing member = {mem_record}")
                elif len(mem_records) > 1:
                    logger.warning(f"Found MULTIPLE MEMBERS :")
                    for i, _m in enumerate(mem_records):
                        logger.warning(f"[{i}]  -  {_m.email} - {_m.name}")
                    index = input("Enter index of which record to use:")
                    mem_record = mem_records[int(index)]
                else:
                    raise MemberRecord.DoesNotExist()

            email = mem_record.email
            logger.info(f"User doesn't exist, using MemberRecord for {name} - {email}")
        except MemberRecord.DoesNotExist:
            logger.warning(f"MemberRecord AND User do not exist, provide manual email:")
            email = input("Enter email").strip()
        user = User.objects.create(name=name, email=email, is_medusa=True, is_staff=True, is_active=True)
    if m.get("Phone Number") and not user.phone_number:
        user.phone_number = m["Phone Number"]
        logger.info(f"setting phone number to {user.phone_number}")
    user.save()
    subcommittee = SubCommittee.objects.get(title=m["Subcommittee"])
    role, created_role = CommitteeRole.objects.get_or_create(
        position=m["Position"], email=m["MeDUSA Email Address"], sub_committee=subcommittee
    )
    if created_role:
        logger.warning(f"Created role : {role}")
    member_rec, created = CommitteeMemberRecord.objects.get_or_create(
        role=role, user=user, year=datetime.datetime.today().year
    )
    member_rec.save()
    logger.info(f"MemberRecord {'created' if created else 'found'} for {user.name}, {user.email} {m['Position']}")
