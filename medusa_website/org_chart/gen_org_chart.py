from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from django.db import IntegrityError

from medusa_website.org_chart.models import CommitteeRole, SubCommittee

EXCEL_FILE = Path(r"I:\GitHub\medusa_website\medusa_website\org_chart\OrgChart.xlsx")
assert EXCEL_FILE.exists()

org_df: pd.DataFrame = pd.read_excel(EXCEL_FILE, sheet_name="For CSV Export")


@dataclass
class RawCommitteeMember:
    name: str
    position: str
    email: str
    sub_committee: str


all_people = [RawCommitteeMember(**row[1]) for row in org_df.iterrows()]
all_people = [p for p in all_people if str(p.name) != "0"]

for mem_raw in all_people:

    try:
        mem_raw.sub_committee = SubCommittee.objects.get(title=mem_raw.sub_committee)
    except SubCommittee.DoesNotExist as exc:
        print(f"Could not create Member due to SubCommittee.DoesNotExist {mem_raw}")
        raise exc
    member = CommitteeRole(**mem_raw.__dict__)
    try:
        member.save()
    except IntegrityError:
        print(f"Already created - {member}")
