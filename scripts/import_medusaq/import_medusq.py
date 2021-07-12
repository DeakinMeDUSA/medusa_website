import logging
import os
import sys

from django.db import IntegrityError

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django

sys.path.append('I:/GitHub/medusa_website')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
logger = logging.getLogger(__name__)

# %%
import csv
from pathlib import Path

from medusa_website.mcq_bank.models import Question, Answer, Category
# IMPORT_FILE = Path(r"I:\GitHub\medusa_website\scripts\import_medusaq\McqData20201017034440.csv")
from medusa_website.users.models import User
from bs4 import UnicodeDammit

user = User.objects.get(id=1)

# IMPORT_FILE = Path(r"I:\GitHub\medusa_website\scripts\import_medusaq\McqData_cleaned.csv")
IMPORT_FILE = Path("/home/medusa_it/medusa_website/scripts/import_medusaq/McqData_cleaned.csv")


def parse_tf(tf: str):
    if tf.upper() == "TRUE":
        return True
    elif tf.upper() == "FALSE":
        return False
    else:
        raise ValueError(f"input was {tf}!")


rows = []

damnit = UnicodeDammit(IMPORT_FILE.read_bytes())
print(f"Detected encoding: {damnit.original_encoding}")
# %%
with open(IMPORT_FILE, "r", encoding=damnit.original_encoding) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        rows.append(row)

headers = rows.pop(0)
headers = [h.lower() for h in headers]
questions_raw = [dict(zip(headers, row)) for row in rows]

# %%


for raw_q in questions_raw:
    explanation = raw_q["correctanswerexplanation"].strip()
    category, _created = Category.objects.get_or_create(name=raw_q["topics"])
    text = raw_q["text"].strip()
    question = Question(text=text,
                        author=None,
                        category=category,
                        explanation=explanation,
                        is_flagged=parse_tf(raw_q["isflagged"])
                        )
    try:
        question.save()
    except IntegrityError:
        continue
    correct_answer = Answer(text=raw_q["correctanswer"].strip(), correct=True, question=question)
    correct_answer.save()
    other_answers = [Answer(text=ans.strip(), correct=False, question=question
                            ) for ans in raw_q["incorrectanswers"].split(";;")]
    for a in other_answers:
        a.save()
