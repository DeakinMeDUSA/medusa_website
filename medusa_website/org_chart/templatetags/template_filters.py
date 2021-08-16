import logging
from typing import Dict

from django import template

logger = logging.getLogger(__name__)

register = template.Library()

import calendar


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, Dict):
        return dictionary.get(key)
    else:
        logger.warning(f"dictionary passed to get_item not a dict! args = {dictionary} , {key}")
        return None


@register.filter
def spaces_to_hyphens_lowercase(string: str):
    return string.replace(" ", "-").lower()


@register.filter
def month_name(month_number):
    return calendar.month_abbr[month_number]
