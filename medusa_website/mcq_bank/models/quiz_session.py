from typing import Optional

from django.db import models
from django.db.models import QuerySet
from django.utils.timezone import now

from medusa_website.mcq_bank.models import Answer
from medusa_website.mcq_bank.models.question import Question
from medusa_website.users.models import User


class QuizSessionExists(RuntimeError):
    pass


class QuizSessionManager(models.Manager):
    def create_session(self, user: User, questions: QuerySet, randomize_order=True):
        if questions.count() < 1:
            raise RuntimeError("Cannot create Quiz Session without any questions!")

        if self.get_current_session(user=user) is not None:
            raise QuizSessionExists(
                "Another QuizSession is currently in progress. Please complete that session before creating another!"
            )

        if randomize_order:
            questions = questions.all().order_by("?")

        new_session: QuizSession = self.create(
            user=user,
            complete=False,
        )
        new_session.save()
        for q in questions.all():
            new_session.questions.add(q)
        new_session.save()
        return new_session

    def get_current_session(self, user: User) -> Optional["QuizSession"]:
        try:
            return self.get(user=user, complete=False)
        except QuizSession.DoesNotExist:
            return None


class QuizSession(models.Model):
    """
    Used to store the progress of logged in users completing some question

    Question_order is a list of integer pks of all the questions in the
    quiz, in order.

    Question_list is a list of integers which represent id's of
    the unanswered questions in csv format.

    Incorrect_questions is a list in the same format.

    Sitting deleted when quiz finished unless quiz.exam_paper is true.

    User_answers is a json object in which the question PK is stored
    with the answer the user gave.
    """

    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
        blank=False,
        related_name="quiz_sessions",
    )
    questions = models.ManyToManyField(
        Question, blank=True, related_name="quiz_sessions"
    )
    answers = models.ManyToManyField(
        Answer, null=True, blank=True, related_name="quiz_sessions"
    )
    complete = models.BooleanField(default=False, verbose_name="Complete")
    started = models.DateTimeField(auto_now_add=True, verbose_name="Session Started")
    finished = models.DateTimeField(null=True, blank=True, verbose_name="Session Ended")
    objects = QuizSessionManager()

    class Meta:
        permissions = (("view_sittings", "Can see completed exams."),)

    @property
    def remaining_questions(self) -> QuerySet[Question]:
        return Question.objects.filter(quiz_sessions=self).exclude(
            answers__in=self.answers.all()
        )

    @property
    def correct_answers(self) -> QuerySet[Answer]:
        return self.answers.filter(correct=True)

    @property
    def incorrect_answers(self):
        return self.answers.filter(correct=False)

    @property
    def current_question(self) -> Optional[Question]:
        """
        Returns the next question, if no question is found, returns None
        """
        if self.remaining_questions.count() == 0:
            return None
        else:
            return self.remaining_questions.first()

    def user_answer_for_question(self, question: Question):
        try:
            return self.answers.get(question=question)
        except Answer.DoesNotExist:
            return None

    @property
    def percent_correct(self) -> float:
        return round(100 * self.correct_answers.count() / self.answers.count(), 2)

    def mark_quiz_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def add_user_answer(self, answer: Answer):
        # Ensure answers can't be added multiple times
        if answer.question.id not in self.questions.values_list("id", flat=True):
            raise RuntimeError(
                "Answer given for a question that isn't in the QuizSession"
            )
        if answer.question.id in self.answers.values_list("question__id", flat=True):
            raise RuntimeError(
                "Answer given is for a question that has already been answered!"
            )
        self.answers.add(answer)
        self.save()
        if self.remaining_questions.count() == 0:
            print("QuizSession complete! Marking complete")
            self.mark_quiz_complete()

    @property
    def progress(self):
        """
        Returns the number of questions answered so far and the total number of
        questions.
        """

        return self.answers.all().count(), self.questions.all().count()
