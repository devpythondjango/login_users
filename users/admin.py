from django.contrib import admin
from .models import (Profile, Faculty, Kafedra, Position,
                     Talimshakli, Student, Teacher, Bolim,
                     System, Hemis, Lms, KeroControl, Building,
                     Application, ApplicationCreate, PositionOne)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_hemis_admin', 'is_moodle_admin', 'is_kerocontrol_admin')
    list_filter = ('is_hemis_admin', 'is_moodle_admin', 'is_kerocontrol_admin')
    search_fields = ('user__username', 'user__email')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Faculty)
admin.site.register(Kafedra)
admin.site.register(Position)
admin.site.register(Talimshakli)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Bolim)
admin.site.register(System)
admin.site.register(Hemis)
admin.site.register(Lms)
admin.site.register(KeroControl)
admin.site.register(Building)
admin.site.register(Application)
admin.site.register(ApplicationCreate)
admin.site.register(PositionOne)
