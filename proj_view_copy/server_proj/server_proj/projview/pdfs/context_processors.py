# myapp/context_processors.py
from django.conf import settings
import os

def host_ip(request):
    return {
        'host_ip': os.getenv('HOST_IP', settings.HOST_IP)
    }
