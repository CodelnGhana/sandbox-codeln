# Generated by Django 2.0.4 on 2019-03-14 13:41

from django.db import migrations
import separatedvaluesfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0011_auto_20190314_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='randomquiz',
            name='questions',
            field=separatedvaluesfield.models.SeparatedValuesField(max_length=150, null=True),
        ),
    ]