from django.contrib import admin
from .models import (Faculty, Kafedra, Position, Profile,
                     Talimshakli, System, Building,
                     Application, ApplicationCreate, PositionOne)

admin.site.register(Profile)
admin.site.register(Faculty)
admin.site.register(Kafedra)
admin.site.register(Position)
admin.site.register(Talimshakli)
admin.site.register(System)
admin.site.register(Building)
admin.site.register(Application)
admin.site.register(ApplicationCreate)
admin.site.register(PositionOne)


