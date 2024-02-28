from django.urls import path

from .views import profile_view, home, application_create, application_list, application_views, xavfsiz

urlpatterns = [
    path('', home, name="home"),
    path('users/profile/', profile_view, name='user_profile'),
    path('application/create/', application_create, name='application_create'),
    path('application/list/', application_list, name='application_list'),
    path('application/views/<int:pk>/', application_views, name='application_views'),
    path('users/xavfsizlik/', xavfsiz, name='xavfsiz'),
]
 


