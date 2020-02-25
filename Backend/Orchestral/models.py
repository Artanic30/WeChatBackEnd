from django.db import models
from django.contrib.auth.models import User
from .constants import TYPE_CHOICE, MEMBER_TYPE


class Identity(models.Model):
    name = models.CharField(max_length=20, unique=True)
    union_id = models.CharField(max_length=100, null=True, blank=True)
    current_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_user', null=True)
    absence_times = models.IntegerField(default=0)
    type = models.CharField(max_length=300, choices=MEMBER_TYPE, default='S')


class Absence(models.Model):
    reason = models.CharField(max_length=300)
    time_absence = models.DateField()
    time_apply = models.DateField(auto_now_add=True)
    result = models.CharField(max_length=300, default='Not processed yet!')
    permission = models.BooleanField(default=False)
    type = models.CharField(max_length=300, choices=TYPE_CHOICE, default='全体排练')
    applier = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='applier')
    processor = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='processor', null=True, blank=True)

    class Meta:
        unique_together = ('applier', 'time_absence')
