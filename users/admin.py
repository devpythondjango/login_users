from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_hemis_admin', 'is_moodle_admin', 'is_kerocontrol_admin')
    list_filter = ('is_hemis_admin', 'is_moodle_admin', 'is_kerocontrol_admin')
    search_fields = ('user__username', 'user__email')

admin.site.register(Profile, ProfileAdmin)

