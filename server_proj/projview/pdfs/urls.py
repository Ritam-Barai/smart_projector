from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    #path('pdfs/', views.list_pdfs, name='list_pdfs'),
    #path('', views.index, name='index')
    path('', views.list_pdfs, name='list_pdfs'),
    path('delete_media_files/', views.delete_media_files, name='delete_media_files'),
]
