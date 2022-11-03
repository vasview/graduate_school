from django.urls import URLPattern, path
from .views import *

urlpatterns = [
    path('supervisor/', ListSupervisorStudents.as_view(), name='supervisor_students'),
]