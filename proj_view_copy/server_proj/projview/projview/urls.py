"""
URL configuration for projview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pdfs import views as pdf_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('pdf_view.urls')),
    path('pdfs/', include('pdfs.urls')),
    path('', pdf_views.index, name='index'),
    path('stop_server/', pdf_views.stop_server, name='stop_server'),
    path('delete_media_files/', pdf_views.delete_media_files, name='delete_media_files'),
    path('health_check/', pdf_views.health_check, name='health_check'),
    path('viewer/', pdf_views.pdf_viewer, name='pdf_viewer'),
    path('log_tab_event/', pdf_views.log_tab_event, name='log_tab_event'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

