from django.urls import path
from .views import index, hemis_arizalar, Ariza_edit, lms_arizalar, kero_arizalar, admin_profile_view
urlpatterns = [
    path('', index, name="index"),
    path('admin/profile/', admin_profile_view, name='admin_profile'),
    path('applications/hemis/', hemis_arizalar, name='hemis_arizalar'),
    path('applications/lms/', lms_arizalar, name='lms_arizalar'),
    path('applications/kero/', kero_arizalar, name='kero_arizalar'),
    path('application/<int:pk>/edit/', Ariza_edit, name='application_edit'),
 
]