from django.urls import path
from . import views
from .pdf_load import PDFViewer 

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    #path('pdfs/', views.list_pdfs, name='list_pdfs'),
    #path('', views.index, name='index')
    path('', views.list_pdfs, name='list_pdfs'),
    path('proj_IP/', views.proj_IP, name='proj_ip'),
    path('stop_server/', views.stop_server, name='stop_server'),
    path('delete_media_files/', views.delete_media_files, name='delete_media_files'),
    path('health_check/', views.health_check, name='health_check'),
    path('viewer/', views.pdf_viewer, name='pdf_viewer'),
    path('render_pdf_page/<str:pdf_name>/<int:page_number>/', views.render_pdf_page_view, name='render_pdf_page'),
    path('log_tab_event/', views.log_tab_event, name='log_tab_event'),
]


