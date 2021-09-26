from typing import Optional

from django_filters.widgets import BooleanWidget


def percent(num, denom, num_digits=2) -> Optional[float]:
    """
    Calculates percent, rounded to num_digits
    :param num: Numerator
    :param denom: Denominator
    :param num_digits: Number of digits to round to. If None, no rounding
    :returns: Float percent, or None if divide by zero occurs
    """
    if denom <= 0:
        return None
    res = 100 * num / denom
    if num_digits is not None:
        return round(res, num_digits)
    else:
        return res


class CustomBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("", "---------"), ("true", "Yes"), ("false", "No"))


def truncate_text(text: str, max_length: int=50):
    if len(text) > max_length:
        return f"{text[0:max_length]} ..."
    else:
        return text
