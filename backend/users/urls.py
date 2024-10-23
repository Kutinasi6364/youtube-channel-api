from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signupview/", views.SignupView.as_view(), name="signup"),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('api/login/', views.login_api_view, name='api_login'),
]
