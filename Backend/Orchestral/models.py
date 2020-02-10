from django.db import models
from django.contrib.auth.models import User
from .constants import TYPE_CHOICE


class Identity(models.Model):
    name = models.CharField(max_length=20, unique=True)
    union_id = models.CharField(max_length=100, null=True, blank=True)
    current_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_user', null=True)


class Absence(models.Model):
    reason = models.CharField(max_length=300)
    time_absence = models.DateField()
    time_apply = models.DateField(auto_now_add=True)
    result = models.CharField(max_length=300, default='Not processed yet!')
    permission = models.BooleanField(default=False)
    type = models.CharField(max_length=300, choices=TYPE_CHOICE, default='A')
    applier = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='applier')
    processor = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='processor', null=True, blank=True)

    class Meta:
        unique_together = ('applier', 'time_absence')
