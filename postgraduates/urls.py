from django.urls import URLPattern, path
from .views import *

app_name = 'postgraduates'

urlpatterns = [
    path('personal_workspace', StudentWorkspace.as_view(), name='student_workspace'),
    path('<int:id>', StudentCard.as_view(), name='show_student_card'),
    path('explanatory_notes/<int:id>/edit', EditExplanatoryNote.as_view(), name='edit_explanatory_note'),
    path('explanatory_notes/show', ShowExplanatoryNote.as_view(), name='show_explanatory_note'),
    path('dissertation_topics/<int:id>/edit', EditDissertationTopic.as_view(), name='edit_dissertation_topic'),
]
