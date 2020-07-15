from django.contrib import admin
from .models import (
    Identity, Absence, NameList,
    PercussionNameList, StringedNameList,
    WindNameList, NotificationEmailList)
# Register your models here.


class IdentityShow(admin.ModelAdmin):
    list_display = ['name']


class NameListShow(admin.ModelAdmin):
    list_display = ['name']


class WindNameListShow(admin.ModelAdmin):
    list_display = ['name']


class StringedNameListShow(admin.ModelAdmin):
    list_display = ['name']


class PercussionNameListShow(admin.ModelAdmin):
    list_display = ['name']


class NotificationEmailListShow(admin.ModelAdmin):
    list_display = ['email']


class AbsenceShow(admin.ModelAdmin):
    list_display = ('reason', 'time_absence', 'time_apply', 'result', 'permission', 'applier', 'processor')


admin.site.register(Identity, IdentityShow)
admin.site.register(Absence, AbsenceShow)
admin.site.register(NameList, NameListShow)
admin.site.register(WindNameList, WindNameListShow)
admin.site.register(StringedNameList, StringedNameListShow)
admin.site.register(PercussionNameList, PercussionNameListShow)
admin.site.register(NotificationEmailList, NotificationEmailListShow)
