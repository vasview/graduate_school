from django.urls import URLPattern, path
from .views import *

urlpatterns = [
    path('', ListApplications.as_view(), name='applications'),
    path('new/', NewApplication.as_view(), name='new_application'),
    path('<int:id>', ShowApplication.as_view(), name='show_application'),
    path('<int:id>/change_status', ChangeStatusApplication.as_view(), name='change_apl_status'),
    path('<int:id>/change_status', ChangeStatusApplication.as_view(), name='change_apl_status'),
    path('search_application/', SearchPostgraduateInApplication.as_view(), name='search_application'),
]