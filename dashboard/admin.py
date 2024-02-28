from django.contrib import admin
from .models import AdminProfile, FileType, Fayl, FaylTasdiq, Author
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','is_self_visible', 'is_admin', 'is_hemis_admin', 'is_lms_admin', 'is_kerocontrol_admin', 'is_admin_kafedra', 'is_admin_talim', 'is_admin_oquv')
    list_filter = ('is_hemis_admin', 'is_lms_admin', 'is_kerocontrol_admin')
    search_fields = ('user__username', 'user__email')


admin.site.register(Fayl)
admin.site.register(AdminProfile, ProfileAdmin)
admin.site.register(FileType)
admin.site.register(FaylTasdiq)
admin.site.register(Author)
