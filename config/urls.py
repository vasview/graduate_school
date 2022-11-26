from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Аспирантура КГTY'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls')),
    path('applications/', include('applications.urls')),
    path('faculty/', include('faculties.urls')),
    path('postgraduates/', include('postgraduates.urls', namespace='postgraduates')),
    path('all_study_plans/', include('study_plans.urls', namespace='all_study_plans')),
    path('student_study_plans/', include('study_plans.urls', namespace='student_study_plans')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
