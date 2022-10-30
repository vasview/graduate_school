from django.urls import URLPattern, path
from .views import *

urlpatterns = [
    path('', ListApplications.as_view(), name='applications'),
    path('new/', NewApplication.as_view(), name='new_application'),
    path('<int:id>', ShowApplication.as_view(), name='show_application'),
    path('<int:id>/edit', EditApplication.as_view(), name='edit_application'),
]