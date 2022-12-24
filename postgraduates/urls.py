from django.urls import URLPattern, path
from .views import *

app_name = 'postgraduates'

urlpatterns = [
    path('personal_workspace', StudentWorkspace.as_view(), name='student_workspace'),

    path('explanatory_notes/create', CreateExplanatoryNote.as_view(), name='create_explanatory_note'),
    path('explanatory_notes/show', ShowExplanatoryNote.as_view(), name='show_explanatory_note'),
    path('explanatory_notes/<int:id>/edit', EditExplanatorySection.as_view(), name='edit_explanatory_note'),
    path('explanatory_notes/<int:id>/remove', DeleteExplanatorySection.as_view(), name='delete_explanatory_note'),
    path('dissertation_topics/<int:id>/edit', EditDissertationTopic.as_view(), name='edit_dissertation_topic'),

    path('supervisor_student/<int:id>', SupervisorStudentCard.as_view(), name='show_student_card'),
    path('supervisor_student/<int:id>/explanatory_note', SupervisorStudentExplanatoryNote.as_view(), name='show_student_explanatory_note'),

    path('explanatory_notes/<int:id>/approve', AjaxUApproveExplanatoryNote.as_view(), name='approve_explanatory_note'),
]
