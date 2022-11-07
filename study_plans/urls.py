from django.urls import URLPattern, path
from .views import *

app_name = 'study_plans'

urlpatterns = [
    path('', ListStudyPlans.as_view(), name='index'),
    path('new', CreateStudyPlan.as_view(), name='create_study_plan'),
    path('<int:id>', ShowStudyPlan.as_view(), name='show_study_plan'),
]