from django.urls import URLPattern, path
from .views import *

app_name = 'study_plans'

urlpatterns = [
    path('', ListStudyPlans.as_view(), name='index'),
    path('new', CreateStudyPlan.as_view(), name='create_study_plan'),
    path('<int:id>', ShowStudyPlan.as_view(), name='show_study_plan'),
    path('work_scope/<int:id>/new_scope_details', AddStudyWorkScopeDetails.as_view(), name='new_scope_details'),

    path('work_scope_details/<int:id>/edit', EditStudyWorkScopeDetails.as_view(), name='edit_scope_details'),
    path('work_scope_details/<int:id>/remove', DeleteStudyWorkScopeDetails.as_view(), name='remove_work_scope_details'),

    path('supervisor_student/plans/<int:id>', ShowSupervisorStudentStudyPlan.as_view(), name='show_supervisor_student_plan'),
    path('works/<int:id>', AjaxUpdateStudyPlanWorkCompletion.as_view(), name='update_work_completion'),
]
