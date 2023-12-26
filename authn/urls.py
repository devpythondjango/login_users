from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import RegisterView, login_admin, login_user, logout_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', login_user, name="login"), 
    path('login/admin/', login_admin, name="login_admin"),
    path('logout/', logout_user, name="logout"),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
