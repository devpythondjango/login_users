from django.contrib import admin
from .models import AdminProfile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','is_self_visible', 'is_admin', 'is_hemis_admin', 'is_lms_admin', 'is_kerocontrol_admin')
    list_filter = ('is_hemis_admin', 'is_lms_admin', 'is_kerocontrol_admin')
    search_fields = ('user__username', 'user__email')

admin.site.register(AdminProfile, ProfileAdmin)
