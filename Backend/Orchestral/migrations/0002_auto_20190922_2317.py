# Generated by Django 2.1.7 on 2019-09-22 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Orchestral', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='processor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processor', to='Orchestral.Identity'),
        ),
    ]
