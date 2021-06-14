from typing import Optional


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
