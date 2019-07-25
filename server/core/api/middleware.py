import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.META.get('HTTP_ACCEPT_TIMEZONE')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
