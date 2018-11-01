from django import template
from django.utils.six.moves.urllib.parse import quote_plus


register = template.Library()

@register.filter
def urlify(value):
	return quote_plus(value)