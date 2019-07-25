from django import template
from django.template.defaultfilters import date, time
from django.utils import timezone

register = template.Library()


@register.simple_tag(takes_context=True)
def has_unread_messages(context, channel):
    """
    Returns True if the channel has any unread messages for the current user.
    Populates the template context with the result in a variable whose
    name is defined by the ``as`` clause.

    Syntax::

        {% has_unread_messages channel as context_name %}
    """
    return channel.has_unread_messages(context.request.user)


@register.filter(expects_localtime=True, is_safe=False)
def dateformat(value):
    """Formats a date according to the given date."""
    if value.date() == timezone.now().date():
        return 'Today, {}'.format(time(value, 'TIME_FORMAT'))
    else:
        return date(value, 'MONTH_DAY_FORMAT')
