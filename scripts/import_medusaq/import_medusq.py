# %%
import csv
from pathlib import Path

from django.db import IntegrityError

from medusa_website.mcq_bank.models import Question, Answer, Category
# IMPORT_FILE = Path(r"I:\GitHub\medusa_website\scripts\import_medusaq\McqData20201017034440.csv")
from medusa_website.users.models import User

user = User.objects.get(id=1)

IMPORT_FILE = Path(r"I:\GitHub\medusa_website\scripts\import_medusaq\McqData_cleaned.csv")


def parse_tf(tf: str):
    if tf.upper() == "TRUE":
        return True
    elif tf.upper() == "FALSE":
        return False
    else:
        raise ValueError(f"input was {tf}!")


rows = []
with open(IMPORT_FILE, "r") as csvfile:
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
