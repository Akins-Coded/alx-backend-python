import logging
from datetime import datetime, timedelta
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
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_tracker = defaultdict(deque) # Tracks Timesamps

        self.time_window = 60 # 60 seconds = 1 minuite
        self.max_messsages = 5 # Maximum messages allowed in the time window
    
    def __call__(self, request):
         # Only track POST requests (assumed to be sending messages)
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            ip = self.get_client_ip(request)
            now = time.time()

            # Remove timestamps older than 60 seconds
            timestamps = self.message_tracker[ip]
            while timestamps and now - timestamps[0] > self.time_window:
                timestamps.popleft()

            # Check if current count exceeds limit
            if len(timestamps) >= self.max_messages:
                return JsonResponse({
                    "error": "⛔ You are Being Rude and Offensive. Please wait before sending more messages."
                }, status=429)

            # Record current message timestamp
            timestamps.append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extracts the client IP address from the request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            allowed_roles = ['admin', 'moderator']
            if not hasattr(user, 'role') or user.role not in allowed_roles:
                return HttpResponse("⛔ You do not have permission to access this Page.", status=403)
            
        return self.get_response(request)