import logging
from typing import Dict

from django import template

logger = logging.getLogger(__name__)

register = template.Library()


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
