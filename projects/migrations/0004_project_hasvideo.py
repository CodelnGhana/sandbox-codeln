# Generated by Django 2.1.5 on 2019-01-29 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20190128_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='hasvideo',
            field=models.BooleanField(default=False),
        ),
    ]