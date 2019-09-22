from django.db import models

# Create your models here.


class Identity(models.Model):
    # todo: uid WeChat API and permissions
    name = models.CharField(max_length=20, unique=True)


class Absence(models.Model):
    reason = models.CharField(max_length=300)
    time_absence = models.DateField()
    time_apply = models.DateField(auto_now_add=True)
    result = models.CharField(max_length=300, default='Not processed yet!')
    permission = models.BooleanField(default=False)
    applier = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='applier')
    processor = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='processor', null=True)

    class Meta:
        unique_together = ('applier', 'time_absence')



