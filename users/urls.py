from django.urls import path

from .views import home, login_user, logout_user, RegisterView, admins, login_admin
from .views import ProfileView, application_create, dashboard, application_list

urlpatterns = [
    path('', home, name="home"),

    path('dashboard/', dashboard, name="dashboard"),

    path('register/', RegisterView.as_view(), name="register"),
    path('login/', login_user, name="login"),
    path('login/admin/', login_admin, name="login_admin"),
    path('logout/', logout_user, name="logout"),

    path('admins/', admins, name="admins"),
    path('profile_user/', ProfileView.as_view(), name='profile_user'),

    path('application/create/', application_create, name='application_create'),
    path('application/list/', application_list, name='application_list'),

]



