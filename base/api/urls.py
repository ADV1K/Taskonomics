from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    # Heartbeat
    path("", views.HeartbeatView.as_view(), name="heartbeat"),
    # Authentication
    path("login/", views.MyTokenObtainPairView.as_view(), name="get_access_token"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh_access_token"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    # Task
    path("task/", views.TaskList.as_view(), name="task-list-and-create"),
    path("task/<int:pk>/", views.TaskDetail.as_view(), name="task-read-update-delete"),
    # Project
    path("project/", views.ProjectList.as_view(), name="project-list-and-create"),
    path("project/<int:pk>/", views.ProjectDetail.as_view(), name="project-read-update-delete"),
]
