import re
from copy import copy
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

CARD_TEMPLATE = Path(
    r"I:\GitHub\medusa_website\medusa_website\org_chart\card_template.html"
).read_text()
ORG_CHART_TEMPATE = Path(
    r"I:\GitHub\medusa_website\medusa_website\org_chart\org_chart_template.html"
).read_text()
OUTPUT_CHART = Path(
    r"I:\GitHub\medusa_website\medusa_website\org_chart\org_chart_output.html"
)
EXCEL_FILE = Path(r"C:\Users\chris\Dropbox\Uni\MEDUSA IT\Org Chart 2021\OrgChart.xlsx")
org_df: pd.DataFrame = pd.read_excel(EXCEL_FILE, sheet_name="For CSV Export")


@dataclass
class Employee:
    name: str
    position: str
    id: int
    manager: str
    email: str
    sub_committee: str
    image: bytes = None
    fill: str = None


all_people = [Employee(**row[1]) for row in org_df.iterrows()]
all_people = [p for p in all_people if str(p.name) != "0"]


def gen_card_div(emp: Employee):
    output_card = copy(CARD_TEMPLATE)
    replace_attrs = ["name", "position", "email"]
    for attr in replace_attrs:
        output_card = re.sub(
            f"%{attr}%", str(getattr(emp, attr)), output_card, flags=re.IGNORECASE
        )
    return output_card


subcommittee_mapping = {
    "Executive Committee": "executive",
    "General Committee": "general",
    "Clinical School Committee": "clinical",
    "Preclinical Committee": "preclinical",
    "Special Interest Groups": "special",
    0: "toplevel",
}

all_cards = {}
for person in all_people:
    if all_cards.get(subcommittee_mapping[person.sub_committee]) is None:
        all_cards[subcommittee_mapping[person.sub_committee]] = []
    all_cards[subcommittee_mapping[person.sub_committee]].append(
        gen_card_div(emp=person)
    )

for subcommittee, sub_cards in all_cards.items():
    ORG_CHART_TEMPATE = re.sub(
        f"<!-- %cards_{subcommittee}% -->",
        "\n".join(sub_cards),
        ORG_CHART_TEMPATE,
        flags=re.IGNORECASE,
    )

# output_html = "\n".join([f"<div>{card}</div>" for card in all_cards])
OUTPUT_CHART.write_text(ORG_CHART_TEMPATE)
