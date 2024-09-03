# middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import PDF
from django.utils import timezone

class SessionEndMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.get_expiry_date() or request.session.get_expiry_date() < timezone.now():
            PDF.objects.all().delete()