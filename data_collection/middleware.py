import time
from django.utils.deprecation import MiddlewareMixin
from .models import PageVisit
import datetime
from django.shortcuts import redirect

class PageVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = time.time()
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_response(self, request, response):
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return response  # Skip admin and static files

        duration_seconds = time.time() - request.start_time
        duration = datetime.timedelta(seconds=duration_seconds)

        # Get additional data
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referer = request.META.get('HTTP_REFERER', '')

        PageVisit.objects.create(
            user=request.user if request.user.is_authenticated else None,
            path=request.path,
            duration=duration,
            ip_address=ip_address,
            user_agent=user_agent,
            referer=referer
        )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class ConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        consent_given = request.session.get('consent_given', False)
        allowed_paths = ['/consent/', '/privacy/', '/accounts/login/', '/accounts/logout/']
        if not consent_given and request.path not in allowed_paths:
            return redirect('consent')
        response = self.get_response(request)
        return response