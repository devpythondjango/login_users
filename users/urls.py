from django.urls import path
from .views import home, login_user, logout_user, profile, RegisterView

urlpatterns = [
  path('', home, name="home"),

  path('register/', RegisterView.as_view(), name="register"),
  path('login/', login_user, name="login"),
  path('logout/', logout_user, name="logout"),

  path('profile/', profile, name='profile'),
]