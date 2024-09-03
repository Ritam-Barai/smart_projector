from django.urls import path
from . import views

urlpatterns = [
    path('', views.pdf_view, name='pdf_viewer'),
]

