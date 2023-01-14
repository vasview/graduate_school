from django.urls import URLPattern, path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('student_profile', ShowStudentProfile.as_view(), name='student_profile'),
    path('edit_student_profile', EditStudentProfile.as_view(), name='edit_student_profile'),
    path('supervisor_profile', ShowSupervisorProfile.as_view(), name='supervisor_profile'),
    path('edit_supervisor_profile', EditSupervisorProfile.as_view(), name='edit_supervisor_profile'),
    path("password_change", PasswordChange.as_view(), name="password_change"),
]
