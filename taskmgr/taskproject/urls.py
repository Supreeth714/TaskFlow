from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tasks import views as tviews
from accounts import views as aviews

urlpatterns = [
    path('admin/', admin.site.urls),
    # API
    path('api/auth/register/', aviews.RegisterAPI.as_view()),
    path('api/auth/token/', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/', include('tasks.api_urls')),
    # Server-rendered UI
    path('', tviews.task_list, name='task_list'),
    path('tasks/new/', tviews.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', tviews.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', tviews.task_delete, name='task_delete'),
    path('tasks/<int:pk>/toggle/', tviews.task_toggle, name='task_toggle'),
    path('login/', aviews.LoginView.as_view(), name='login'),
    path('logout/', aviews.logout_view, name='logout'),
    path('register/', aviews.register_view, name='register'),
]
