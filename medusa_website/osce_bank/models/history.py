from django.db import models

from medusa_website.osce_bank.models.osce_station import OSCEStation
from medusa_website.users.models import User


class OSCEHistory(models.Model):
    """
    History of completed OSCE station

    """

    user = models.OneToOneField(User, verbose_name="User", on_delete=models.PROTECT, related_name="osce_history")

    completed_stations = models.ManyToManyField(OSCEStation, related_name="osce_user_histories")

    class Meta:
        verbose_name = "OSCE User History"
        verbose_name_plural = "OSCE User Histories"

    # @property
    # @memoize(timeout=120)  # cache result for 120 seconds
    # def category_progress(self) -> List[Dict[str, Optional[float]]]:
    #     """
    #     Returns a dict in which the key is the category name and the item is a dict of results, along with an aggregated "all"
    #
    #     """
    #     from medusa_website.osce_bank.models import OSCEStation, Record
    #
    #     cat_progress = []
    #
    #     all_qs = OSCEStation.objects.all()
    #     all_qs_count = all_qs.count()
    #     answered_qs = Record.objects.filter(user=self.user).prefetch_related("answer", "osce_station__category")
    #     distinct_answers = answered_qs.distinct("osce_station")
    #     distinct_answers_count = distinct_answers.count()
    #     all_attempted_percent = percent(distinct_answers_count, all_qs_count)
    #     all_correct_q = [r for r in answered_qs if r.is_correct]
    #     all_average_score = percent(len(all_correct_q), answered_qs.count())
    #     cat_progress.append(
    #         {
    #             "id": 0,
    #             "name": "OVERALL",
    #             "cat_qs_num": all_qs_count,
    #             "attempted_num": distinct_answers_count,
    #             "attempted_percent": all_attempted_percent,
    #             "cat_average_score": all_average_score,
    #         }
    #     )
    #
    #     for cat in Category.objects.all().prefetch_related("osce_stations"):
    #         all_cat_qs = cat.osce_stations.all()
    #         all_cat_qs_count = all_cat_qs.count()
    #         answered = answered_qs.filter(osce_station__category=cat)
    #         distinct_answers = answered.distinct("osce_station")
    #         distinct_answers_count = distinct_answers.count()
    #         cat_attempted_percent = percent(distinct_answers_count, all_cat_qs_count)
    #         correct_q = [r for r in answered if r.is_correct]
    #         cat_average_score = percent(len(correct_q), answered.count())
    #         cat_progress.append(
    #             {
    #                 "id": cat.id,
    #                 "name": cat.name,
    #                 "cat_qs_num": all_cat_qs_count,
    #                 "attempted_num": distinct_answers_count,
    #                 "attempted_percent": cat_attempted_percent,
    #                 "cat_average_score": cat_average_score,
    #             }
    #         )
    #
    #     return cat_progress
    #
    # @property
    # def session_history(
    #     self,
    # ) -> List[Dict[str, Union[None, float, bool, datetime.datetime]]]:
    #     """
    #     Returns a dict in which the key is the category name and the item is a dict of results
    #
    #     """
    #     session_history = []
    #
    #     for session in self.quiz_sessions:
    #         attempted = session.answers.count()
    #
    #         session_history.append(
    #             {
    #                 "id": session.id,
    #                 "is_complete": session.complete,
    #                 "started": session.started,
    #                 "finished": session.finished,
    #                 "total_session_qs": session.osce_stations.count(),
    #                 "attempted": session.answers.count(),
    #                 "correct_answers": session.correct_answers.count(),
    #                 "correct_answers_percent": session.percent_correct,
    #             }
    #         )
    #     return list(reversed(session_history))
