from django.urls import URLPattern, path
from .views import *

urlpatterns = [
    path('<int:id>', StudentCard.as_view(), name='show_student_card'),
    path('<int:id>/explanatory_notes/new', EditExplanatoryNote.as_view(), name='edit_explanatory_note'),
    path('<int:id>/explanatory_notes/show', ShowExplanatoryNote.as_view(), name='show_explanatory_note'),
]