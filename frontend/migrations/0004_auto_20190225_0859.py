# Generated by Django 2.1.5 on 2019-02-25 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_submissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissions',
            name='candidate',
        ),
        migrations.RemoveField(
            model_name='submissions',
            name='transaction',
        ),
        migrations.DeleteModel(
            name='submissions',
        ),
    ]