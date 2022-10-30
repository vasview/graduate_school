from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Аспирантура КГTY'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls')),
    path('applications/', include('applications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)