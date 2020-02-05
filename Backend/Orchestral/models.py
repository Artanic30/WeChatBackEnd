from django.db import models
from django.contrib.auth.models import User


class Identity(models.Model):
    name = models.CharField(max_length=20, unique=True)
    union_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    current_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_user', null=True)


class Absence(models.Model):
    reason = models.CharField(max_length=300)
    time_absence = models.DateField()
    time_apply = models.DateField(auto_now_add=True)
    result = models.CharField(max_length=300, default='Not processed yet!')
    permission = models.BooleanField(default=False)
    applier = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='applier')
    processor = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='processor', null=True, blank=True)

    class Meta:
        unique_together = ('applier', 'time_absence')



