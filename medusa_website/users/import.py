import re
from itertools import islice
from pathlib import Path

import pandas as pd
from django.conf import settings
from openpyxl import load_workbook

# %%
REPORT_PATH = Path(
    settings.MEDIA_ROOT, "users", "Club Weekly Membership Report Schedule.xlsx"
)


def extract_subscription_type(sub_row: str):
    sub_type = re.findall(r"Medical Student.*", sub_row, flags=re.IGNORECASE)[0]
    sub_type = sub_type.replace("Subscription", "").strip()
    return sub_type


def read_dusa_report():
    if REPORT_PATH.exists() is False:
        raise FileNotFoundError(f"Could not find report excel file at {REPORT_PATH}")
    wb = load_workbook(REPORT_PATH)
    data = wb["Report"].values
    cols = next(data)[1:]
    data = list(data)
    data = (islice(r, 1, None) for r in data)
    df = pd.DataFrame(data, columns=cols)
    df["Subscription Type"] = df["Subscription Type"].map(extract_subscription_type)

    return df


# %%


def create_google_group_export(dusa_report: pd.DataFrame):
    google_export = pd.DataFrame(
        columns=["Member Email", "Member Type", "Member Role", "Group Email [Required]"]
    )
    google_export["Member Email"] = dusa_report["Email"]
    google_export["Member Type"] = "USER"
    google_export["Member Role"] = "MEMBER"
    google_export["Group Email [Required]"] = "medusa-members@medusa.org.au"
    return google_group_export


# %%


if __name__ == "__main__":
    DUSA_REPORT = read_dusa_report()
    DUSA_REPORT.to_csv(REPORT_PATH.with_suffix(".csv"), index=False)
    google_group_export = create_google_group_export(DUSA_REPORT)
    google_group_export.to_csv(
        REPORT_PATH.with_name("medusa_members_google_group.csv"), index=False
    )
