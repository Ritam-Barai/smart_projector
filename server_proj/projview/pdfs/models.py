from django.db import models
from django.contrib.sessions.models import Session
from .storage import OverwriteStorage

class PDF(models.Model):
    file = models.FileField(upload_to='pdfs/', storage=OverwriteStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file.name
    
    
    '''
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    #request.session.setdefault('key', 'default_value')
    some_field = models.CharField(max_length=200, default='default_value')
    '''
