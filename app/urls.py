from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]