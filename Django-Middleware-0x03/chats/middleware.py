import logging
from datetime import datetime
from django.http import HttpResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Configure logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = datetime.strptime("18:00", "%H:%M").time()  # 6PM
        end_time = datetime.strptime("21:00", "%H:%M").time()    # 9PM

        if not (start_time <= current_time <= end_time):
            return HttpResponse("⛔ Access restricted. You can only access this app between 6PM and 9PM.", status=403)

        return self.get_response(request)
