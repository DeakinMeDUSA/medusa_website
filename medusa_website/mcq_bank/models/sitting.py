import json

from django.core.exceptions import ImproperlyConfigured
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.utils.timezone import now

from medusa_website.mcq_bank.models.question import Question
from medusa_website.mcq_bank.models.quiz import Quiz
from medusa_website.users.models import User


class SittingManager(models.Manager):
    def new_sitting(self, user: User, quiz: Quiz):
        if quiz.random_order is True:
            question_set = quiz.questions.all().order_by("?")
        else:
            question_set = quiz.questions.all()

        question_set = [item.id for item in question_set]

        if len(question_set) == 0:
            raise ImproperlyConfigured(
                "Question set of the quiz is empty. "
                "Please configure questions properly"
            )

        if quiz.max_questions and quiz.max_questions < len(question_set):
            question_set = question_set[: quiz.max_questions]

        questions = ",".join(map(str, question_set)) + ","

        new_sitting = self.create(
            user=user,
            quiz=quiz,
            question_order=questions,
            question_list=questions,
            incorrect_questions="",
            current_score=0,
            complete=False,
            user_answers="{}",
        )
        return new_sitting

    def user_sitting(self, user, quiz):
        if (
            quiz.single_attempt is True
            and self.filter(user=user, quiz=quiz, complete=True).exists()
        ):
            return False
        try:
            sitting = self.get(user=user, quiz=quiz, complete=False)
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(user, quiz)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(user=user, quiz=quiz, complete=False)[0]
        return sitting


class Sitting(models.Model):
    """
    Used to store the progress of logged in users sitting a quiz.
    Replaces the session system used by anon users.

    Question_order is a list of integer pks of all the questions in the
    quiz, in order.

    Question_list is a list of integers which represent id's of
    the unanswered questions in csv format.

    Incorrect_questions is a list in the same format.

    Sitting deleted when quiz finished unless quiz.exam_paper is true.

    User_answers is a json object in which the question PK is stored
    with the answer the user gave.
    """

    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz, verbose_name="Quiz", on_delete=models.CASCADE)

    question_order = models.CharField(
        max_length=1024,
        verbose_name="Question Order",
        validators=[validate_comma_separated_integer_list],
    )

    question_list = models.CharField(
        max_length=1024,
        verbose_name="Question List",
        validators=[validate_comma_separated_integer_list],
    )

    incorrect_questions = models.CharField(
        max_length=1024,
        blank=True,
        verbose_name="Incorrect questions",
        validators=[validate_comma_separated_integer_list],
    )

    current_score = models.IntegerField(verbose_name="Current Score")

    complete = models.BooleanField(default=False, blank=False, verbose_name="Complete")

    user_answers = models.TextField(
        blank=True, default="{}", verbose_name="User Answers"
    )

    start = models.DateTimeField(auto_now_add=True, verbose_name="Start")

    end = models.DateTimeField(null=True, blank=True, verbose_name="End")

    objects = SittingManager()

    class Meta:
        permissions = (("view_sittings", "Can see completed exams."),)

    def get_first_question(self):
        """
        Returns the next question.
        If no question is found, returns False
        Does NOT remove the question from the front of the list.
        """
        if not self.question_list:
            return False

        first, _ = self.question_list.split(",", 1)
        question_id = int(first)
        return Question.objects.get(id=question_id)

    def remove_first_question(self):
        if not self.question_list:
            return

        _, others = self.question_list.split(",", 1)
        self.question_list = others
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    @property
    def get_current_score(self):
        return self.current_score

    def _question_ids(self):
        return [int(n) for n in self.question_order.split(",") if n]

    @property
    def get_percent_correct(self):
        dividend = float(self.current_score)
        divisor = len(self._question_ids())
        if divisor < 1:
            return 0  # prevent divide by zero error

        if dividend > divisor:
            return 100

        correct = int(round((dividend / divisor) * 100))

        if correct >= 1:
            return correct
        else:
            return 0

    def mark_quiz_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def add_incorrect_question(self, question):
        """
        Adds uid of incorrect question to the list.
        The question object must be passed in.
        """
        if len(self.incorrect_questions) > 0:
            self.incorrect_questions += ","
        self.incorrect_questions += str(question.id) + ","
        if self.complete:
            self.add_to_score(-1)
        self.save()

    @property
    def get_incorrect_questions(self):
        """
        Returns a list of non empty integers, representing the pk of
        questions
        """
        return [int(q) for q in self.incorrect_questions.split(",") if q]

    def remove_incorrect_question(self, question):
        current = self.get_incorrect_questions
        current.remove(question.id)
        self.incorrect_questions = ",".join(map(str, current))
        self.add_to_score(1)
        self.save()

    @property
    def check_if_passed(self):
        return self.get_percent_correct >= self.quiz.pass_mark

    @property
    def result_message(self):
        if self.check_if_passed:
            return self.quiz.success_text
        else:
            return self.quiz.fail_text

    def add_user_answer(self, question, guess):
        current = json.loads(self.user_answers)
        current[question.id] = guess
        self.user_answers = json.dumps(current)
        self.save()

    def get_questions(self, with_answers=False):
        question_ids = self._question_ids()
        questions = sorted(
            self.quiz.questions.filter(id__in=question_ids).select_subclasses(),
            key=lambda q: question_ids.index(q.id),
        )

        if with_answers:
            user_answers = json.loads(self.user_answers)
            for question in questions:
                question.user_answer = user_answers[str(question.id)]

        return questions

    @property
    def questions_with_user_answers(self):
        return {q: q.user_answer for q in self.get_questions(with_answers=True)}

    @property
    def get_max_score(self):
        return len(self._question_ids())

    def progress(self):
        """
        Returns the number of questions answered so far and the total number of
        questions.
        """
        answered = len(json.loads(self.user_answers))
        total = self.get_max_score
        return answered, total
