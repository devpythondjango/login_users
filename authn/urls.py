from django.urls import path
from .views import RegisterView, login_admin, login_user, logout_user, captcha_image


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', login_user, name="login"),
    path('captcha/', captcha_image, name='captcha_image'),
    path('login/admin/', login_admin, name="login_admin"),
    path('logout/', logout_user, name="logout"),

]