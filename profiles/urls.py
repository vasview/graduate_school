from django.urls import URLPattern, path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('student_profile', ShowStudentProfile.as_view(), name='student_profile'),
]
