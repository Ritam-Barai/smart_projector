from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    #path('pdfs/', views.list_pdfs, name='list_pdfs'),
    #path('', views.index, name='index')
    path('', views.list_pdfs, name='list_pdfs'),
    path('proj_IP/', views.proj_IP, name='proj_ip'),
    path('stop_server/', views.stop_server, name='stop_server'),
    path('delete_media_files/', views.delete_media_files, name='delete_media_files'),
]
