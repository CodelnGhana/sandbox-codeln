# Generated by Django 2.0.4 on 2019-01-10 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_auto_20190110_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opencall',
            name='transaction',
            field=models.IntegerField(),
        ),
    ]
