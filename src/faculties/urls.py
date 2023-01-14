from django.urls import URLPattern, path
from .views import *

urlpatterns = [
    path('supervisor/students', ListSupervisorStudents.as_view(), name='supervisor_students'),
    path('search_supervisor_student/', SearchSupervisorStudents.as_view(), name='search_supervisor_student'),
]