# import logging
# from typing import Optional
#
# from django.db import models
# from django.db.models import QuerySet
# from django.urls import reverse
# from django.utils.timezone import now
#
# from medusa_website.users.models import User
#
# logger = logging.getLogger(__name__)
#
#
# class OSCESessionExists(RuntimeError):
#     pass
#
#
# class OSCESession(models.Model):
#     """
#     Used to store the progress of logged in users completing some osce_stations
#
#     OSCEStation_order is a list of integer pks of all the osce_stations in the
#     quiz, in order.
#
#     OSCEStation_list is a list of integers which represent id's of
#     the unanswered osce_stations in csv format.
#
#     Incorrect_osce_stations is a list in the same format.
#
#     User_answers is a json object in which the osce_station PK is stored
#     with the answer the user gave.
#     """
#
#     user = models.ForeignKey(
#         User,
#         verbose_name="User",
#         on_delete=models.PROTECT,
#         blank=False,
#         related_name="quiz_sessions",
#     )
#     osce_stations = models.ManyToManyField(OSCEStation, blank=True, related_name="quiz_sessions")
#     answers = models.ManyToManyField(Answer, blank=True, related_name="quiz_sessions")
#     complete = models.BooleanField(default=False, verbose_name="Complete")
#     started = models.DateTimeField(auto_now_add=True, verbose_name="Session Started")
#     finished = models.DateTimeField(null=True, blank=True, verbose_name="Session Ended")
#     current_osce_station_index = models.IntegerField(blank=False, null=False, default=0,
#                                                  verbose_name="Index of the osce_station currently being answered")
#
#     def increment_osce_station_index(self, save=True):
#         self.current_osce_station_index += 1
#         if save:
#             self.save()
#
#     def decrement_osce_station_index(self, save=True):
#         self.current_osce_station_index -= 1
#         if save:
#             self.save()
#
#     def osce_station_at_index(self, index: int):
#         if index < 0:  # Otherwise we'll return items from the other end of the list
#             logger.warning(f"Could not get osce_station at index {index}")
#             return None
#         try:
#             return list(self.osce_stations.all())[index]
#         except IndexError:
#             logger.warning(f"Could not get osce_station at index {index}")
#             return None
#
#     @property
#     def unanswered_osce_stations(self) -> QuerySet[OSCEStation]:
#         return OSCEStation.objects.filter(quiz_sessions=self).exclude(answers__in=self.answers.all())
#
#     @property
#     def answered_osce_stations(self) -> QuerySet[OSCEStation]:
#         return OSCEStation.objects.filter(quiz_sessions=self, answers__in=self.answers.all())
#
#     @property
#     def correct_answers(self) -> QuerySet[Answer]:
#         return self.answers.filter(correct=True)
#
#     @property
#     def incorrect_answers(self):
#         return self.answers.filter(correct=False)
#
#     @property
#     def current_osce_station(self) -> Optional[OSCEStation]:
#         """
#         Returns the current osce_station, note that this osce_station isn't necessarily un-answered or present
#         """
#         return self.osce_station_at_index(self.current_osce_station_index)
#
#     @property
#     def current_osce_station_response(self) -> Optional[Answer]:
#         """
#         Returns the current osce_station's answer or None
#         """
#         try:
#             return self.answers.all().get(osce_station=self.current_osce_station)
#         except Answer.DoesNotExist:
#             return None
#
#     @property
#     def current_osce_station_answered(self) -> bool:
#         if q := self.current_osce_station:
#             return q in self.answered_osce_stations
#         else:
#             return False
#
#     @property
#     def next_osce_station_index(self) -> Optional[int]:
#         if self.current_osce_station_index < self.osce_stations.count() - 1:
#             return self.current_osce_station_index + 1
#         else:
#             return None
#
#     @property
#     def previous_osce_station_index(self) -> Optional[int]:
#         if self.current_osce_station_index > 0:
#             return self.current_osce_station_index - 1
#         else:
#             return None
#
#     def user_answer_for_osce_station(self, osce_station: OSCEStation):
#         try:
#             return self.answers.get(osce_station=osce_station)
#         except Answer.DoesNotExist:
#             return None
#
#     @property
#     def percent_correct(self) -> float:
#         if self.answers.count() == 0:
#             return 0.0
#         else:
#             return round(100 * self.correct_answers.count() / self.answers.count(), 2)
#
#     def mark_quiz_complete(self):
#         self.complete = True
#         self.finished = now()
#         self.save()
#
#     def add_user_answer(self, answer: Answer):
#         # Ensure answers can't be added multiple times
#         if answer.osce_station.id not in self.osce_stations.values_list("id", flat=True):
#             raise RuntimeError("Answer given for a osce_station that isn't in the OSCESession")
#         if answer.osce_station.id in self.answers.values_list("osce_station__id", flat=True):
#             raise RuntimeError("Answer given is for a osce_station that has already been answered!")
#         self.answers.add(answer)
#         if self.current_osce_station_index < self.osce_stations.count() - 1:
#             self.increment_osce_station_index(save=False)
#         self.save()
#         ans_rec = Record(user=self.user, answer=answer, osce_station=answer.osce_station)
#         ans_rec.save()
#         if self.unanswered_osce_stations.count() == 0:
#             print("OSCESession complete! Marking complete")
#             self.mark_quiz_complete()
#
#     @property
#     def progress(self):
#         """
#         Returns the number of osce_stations answered so far and the total number of
#         osce_stations.
#         """
#
#         return self.answers.all().count(), self.osce_stations.all().count()
#
#     @classmethod
#     def get_current(cls, user: User) -> Optional["OSCESession"]:
#         try:
#             return cls.objects.get(user=user, complete=False)
#         except (OSCESession.DoesNotExist, TypeError):
#             return None
#
#     @property
#     def is_current(self):
#         return not self.complete
#
#     @classmethod
#     def check_no_current_session(cls, user: User):
#         if cls.get_current(user=user) is not None:
#             raise OSCESessionExists(
#                 "Another OSCESession is currently in progress. Please complete that session before creating another!"
#             )
#
#     @classmethod
#     def create_from_osce_stations(
#         cls, user: User, osce_stations: QuerySet, max_n=20, randomise_order=True, include_answered=False, save=True
#     ) -> "OSCESession":
#         cls.check_no_current_session(user=user)
#
#         if include_answered is False:
#             osce_stations = osce_stations.exclude(records__in=Record.objects.filter(user=user))
#
#         if randomise_order is True:
#             osce_stations = osce_stations.order_by("?")
#
#         max_n = max_n if max_n <= osce_stations.count() else osce_stations.count()
#         selected_qs = osce_stations[0: max_n + 1]
#
#         if selected_qs.count() < 1:
#             raise RuntimeError("Cannot create OSCE Session without any osce_stations!")
#
#         session = cls(user=user)
#         session.save()
#         session.osce_stations.set(selected_qs)
#         session.save()
#         return session
#
#     @classmethod
#     def create_from_categories(
#         cls,
#         user: User,
#         categories: QuerySet,
#         max_n=20,
#         randomise_order=True,
#         include_answered=False,
#     ) -> "OSCESession":
#         cls.check_no_current_session(user=user)
#         osce_stations = OSCEStation.objects.filter(category__in=categories)
#
#         return cls.create_from_osce_stations(
#             user=user,
#             osce_stations=osce_stations,
#             max_n=max_n,
#             randomise_order=randomise_order,
#             include_answered=include_answered,
#         )
#
#     def get_absolute_url(self):
#         return reverse("osce_bank:quiz_session_detail", kwargs={"id": self.id})
#
#     def __repr__(self):
#         return f"<OSCESession: OSCESession object ({self.id}), Q index={self.current_osce_station_index}>"
