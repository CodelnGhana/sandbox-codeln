# Generated by Django 2.0.4 on 2019-01-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_remove_applications_stage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opencall',
            name='stage',
        ),
        migrations.AddField(
            model_name='applications',
            name='stage',
            field=models.CharField(default='requirements met', max_length=100),
        ),
    ]
