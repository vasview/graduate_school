from django.urls import URLPattern, path
from .views import *

app_name = 'study_plans'

urlpatterns = [
    path('', ListStudyPlans.as_view(), name='index'),
    path('new', CreateStudyPlan.as_view(), name='create_study_plan'),
    path('<int:id>', ShowStudyPlan.as_view(), name='show_study_plan'),
    path('work_scope/<int:id>/new_scope_details', AddStudyWorkScopeDetails.as_view(), name='new_scope_details'),
    path('work_scope/<int:id>/new_scope_subject', AddStudyWorkScopeSubject.as_view(), name='new_scope_subject'),

    path('work_scope_details/<int:id>/remove', DeleteStudyWorkScopeDetails.as_view(), name='remove_work_scope_details'),
]
