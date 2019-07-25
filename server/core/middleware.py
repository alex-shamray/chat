import logging
import socket
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if response.get('Content-Type') == 'application/json':
            if getattr(response, 'streaming', False):
                response_body = '<<<Streaming>>>'
            else:
                response_body = response.content
        else:
            response_body = '<<<Not JSON>>>'

        log_data = {
            'user': request.user.pk,

            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),
            'user_agent': request.META.get('HTTP_USER_AGENT'),

            'request_method': request.method,
            'request_path': request.get_full_path(),
            'request_body': request.POST,

            'response_status': response.status_code,
            'response_body': response_body,

            'run_time': time.time() - request.start_time,
        }

        logger.debug(str(log_data))

        return response
