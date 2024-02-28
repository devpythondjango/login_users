from django.urls import path
from .views import (
    index, hemis_arizalar, Ariza_edit,
    lms_arizalar, kero_a_arizalar, admin_profile_view,
    yuklash_sahifasi, fayllar, teacher, get_authors,
    edit_input, fayl_detail, tasdiqlash,
    fayl_tasdiq, kero_c_arizalar, vaucher_arizalar

)

urlpatterns = [
    path('', index, name="index"),
    path('admin/profile/', admin_profile_view, name='admin_profile'),
    path('applications/hemis/', hemis_arizalar, name='hemis_arizalar'),
    path('applications/lms/', lms_arizalar, name='lms_arizalar'),
    path('applications/A-bino/kerio/', kero_a_arizalar, name='kero_a_arizalar'),
    path('applications/C-bino/kerio/', kero_c_arizalar, name='kero_c_arizalar'),
    path('applications/vaucher_arizalar/', vaucher_arizalar, name='vaucher_arizalar'),
    path('application/<int:pk>/edit/', Ariza_edit, name='application_edit'),

    path('admin/fileinput/', yuklash_sahifasi, name='yuklash_sahifasi'),
    path('admin/files/', fayllar, name='files'),
    path('admin/teacher/', teacher, name='teacher'),
    path('get_authors/', get_authors, name='get_authors'),

    path('admin/fileinput//<int:pk>/edit/', edit_input, name='edit_input'),

    path('admin/fayl/', fayl_tasdiq, name='fayl_tasdiq'),
    path('fayl/<int:fayl_id>/', fayl_detail, name='fayl_detail'),
    path('fayl/<int:fayl_id>/tasdiqlash/', tasdiqlash, name='tasdiqlash'),
]