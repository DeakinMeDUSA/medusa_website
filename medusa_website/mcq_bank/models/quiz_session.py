import logging
from typing import Optional

from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now

from medusa_website.mcq_bank.models.answer import Answer
from medusa_website.mcq_bank.models.question import Question
from medusa_website.mcq_bank.models.record import Record
from medusa_website.users.models import User

logger = logging.getLogger(__name__)


class QuizSessionExists(RuntimeError):
    pass


class QuizSession(models.Model):
    """
    Used to store the progress of logged in users completing some questions

    Question_order is a list of integer pks of all the questions in the
    quiz, in order.

    Question_list is a list of integers which represent id's of
    the unanswered questions in csv format.

    Incorrect_questions is a list in the same format.

    User_answers is a json object in which the question PK is stored
    with the answer the user gave.
    """

    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.PROTECT,
        blank=False,
        related_name="quiz_sessions",
    )
    questions = models.ManyToManyField(Question, blank=True, related_name="quiz_sessions")
    answers = models.ManyToManyField(Answer, blank=True, related_name="quiz_sessions")
    complete = models.BooleanField(default=False, verbose_name="Complete")
    started = models.DateTimeField(auto_now_add=True, verbose_name="Session Started")
    finished = models.DateTimeField(null=True, blank=True, verbose_name="Session Ended")
    current_question_index = models.IntegerField(
        blank=False, null=False, default=0, verbose_name="Index of the question currently being answered"
    )

    def increment_question_index(self, save=True):
        self.current_question_index += 1
        if save:
            self.save()

    def decrement_question_index(self, save=True):
        self.current_question_index -= 1
        if save:
            self.save()

    def question_at_index(self, index: int):
        if index < 0:  # Otherwise we'll return items from the other end of the list
            logger.warning(f"Could not get question at index {index}")
            return None
        try:
            return list(self.questions.all())[index]
        except IndexError:
            logger.warning(f"Could not get question at index {index}")
            return None

    @property
    def unanswered_questions(self) -> QuerySet[Question]:
        return Question.objects.filter(quiz_sessions=self).exclude(answers__in=self.answers.all())

    @property
    def answered_questions(self) -> QuerySet[Question]:
        return Question.objects.filter(quiz_sessions=self, answers__in=self.answers.all())

    @property
    def correct_answers(self) -> QuerySet[Answer]:
        return self.answers.filter(correct=True)

    @property
    def incorrect_answers(self):
        return self.answers.filter(correct=False)

    @property
    def current_question(self) -> Optional[Question]:
        """
        Returns the current question, note that this question isn't necessarily un-answered or present
        """
        return self.question_at_index(self.current_question_index)

    @property
    def current_question_response(self) -> Optional[Answer]:
        """
        Returns the current question's answer or None
        """
        try:
            return self.answers.all().get(question=self.current_question)
        except Answer.DoesNotExist:
            return None

    @property
    def current_question_answered(self) -> bool:
        if q := self.current_question:
            return q in self.answered_questions
        else:
            return False

    @property
    def next_question_index(self) -> Optional[int]:
        if self.current_question_index < self.questions.count() - 1:
            return self.current_question_index + 1
        else:
            return None

    @property
    def previous_question_index(self) -> Optional[int]:
        if self.current_question_index > 0:
            return self.current_question_index - 1
        else:
            return None

    def user_answer_for_question(self, question: Question):
        try:
            return self.answers.get(question=question)
        except Answer.DoesNotExist:
            return None

    @property
    def percent_correct(self) -> float:
        if self.answers.count() == 0:
            return 0.0
        else:
            return round(100 * self.correct_answers.count() / self.answers.count(), 2)

    def mark_quiz_complete(self):
        self.complete = True
        self.finished = now()
        self.save()

    def add_user_answer(self, answer: Answer):
        # Ensure answers can't be added multiple times
        if answer.question.id not in self.questions.values_list("id", flat=True):
            raise RuntimeError("Answer given for a question that isn't in the QuizSession")
        if answer.question.id in self.answers.values_list("question__id", flat=True):
            raise RuntimeError("Answer given is for a question that has already been answered!")
        self.answers.add(answer)
        if self.current_question_index < self.questions.count() - 1:
            self.increment_question_index(save=False)
        self.save()
        ans_rec = Record(user=self.user, answer=answer, question=answer.question)
        ans_rec.save()
        if self.unanswered_questions.count() == 0:
            print("QuizSession complete! Marking complete")
            self.mark_quiz_complete()

    @property
    def progress(self):
        """
        Returns the number of questions answered so far and the total number of
        questions.
        """

        return self.answers.all().count(), self.questions.all().count()

    @classmethod
    def get_current(cls, user: User) -> Optional["QuizSession"]:
        try:
            return cls.objects.get(user=user, complete=False)
        except (QuizSession.DoesNotExist, TypeError):
            return None

    @property
    def is_current(self):
        return not self.complete

    @classmethod
    def check_no_current_session(cls, user: User):
        if cls.get_current(user=user) is not None:
            raise QuizSessionExists(
                "Another QuizSession is currently in progress. Please complete that session before creating another!"
            )

    @classmethod
    def create_from_questions(
        cls, user: User, questions: QuerySet, max_n=20, randomise_order=True, include_answered=False, save=True
    ) -> "QuizSession":
        cls.check_no_current_session(user=user)

        if include_answered is False:
            questions = questions.exclude(records__in=Record.objects.filter(user=user))

        if randomise_order is True:
            questions = questions.order_by("?")

        max_n = max_n if max_n <= questions.count() else questions.count()
        selected_qs = questions[0 : max_n + 1]

        if selected_qs.count() < 1:
            raise RuntimeError("Cannot create Quiz Session without any questions!")

        session = cls(user=user)
        session.save()
        session.questions.set(selected_qs)
        session.save()
        return session

    @classmethod
    def create_from_categories(
        cls,
        user: User,
        categories: QuerySet,
        max_n=20,
        randomise_order=True,
        include_answered=False,
    ) -> "QuizSession":
        cls.check_no_current_session(user=user)
        questions = Question.objects.filter(category__in=categories)

        return cls.create_from_questions(
            user=user,
            questions=questions,
            max_n=max_n,
            randomise_order=randomise_order,
            include_answered=include_answered,
        )

    def get_absolute_url(self):
        return reverse("mcq_bank:quiz_session_detail", kwargs={"id": self.id})

    def __repr__(self):
        return f"<QuizSession: QuizSession object ({self.id}), Q index={self.current_question_index}>"
