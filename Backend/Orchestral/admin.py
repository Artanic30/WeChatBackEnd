from django.contrib import admin
from .models import Identity, Absence

# Register your models here.


class IdentityShow(admin.ModelAdmin):
    list_display = ['name']


class AbsenceShow(admin.ModelAdmin):
    list_display = ('reason', 'time_absence', 'time_apply', 'result', 'permission', 'applier', 'processor')


admin.site.register(Identity, IdentityShow)
admin.site.register(Absence, AbsenceShow)
