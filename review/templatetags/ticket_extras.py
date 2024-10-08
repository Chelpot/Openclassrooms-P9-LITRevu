from django import template
from django.utils import timezone
import locale
locale.setlocale(locale.LC_TIME,'')

register = template.Library()

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
ICON_STAR_RATING = '★'
ICON_STAR_RATING_EMPTY = '☆'
MAX_NB_STAR_RATING = 5

@register.filter
def model_type(value):
    return type(value).__name__

@register.filter
def get_posted_at_display(posted_at):
    seconds_ago = (timezone.now() - posted_at).total_seconds()
    if seconds_ago <= HOUR:
        return f'Publié il y a {int(seconds_ago // MINUTE)} minutes.'
    elif seconds_ago <= DAY:
        return f'Publié il y a {int(seconds_ago // HOUR)} heures.'
    return f'{posted_at.strftime("%Hh%M, %d %B %Y")}'

@register.filter
def get_rating(nb_star):
    return nb_star*ICON_STAR_RATING + (5-nb_star)*ICON_STAR_RATING_EMPTY
