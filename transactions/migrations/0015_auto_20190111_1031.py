# Generated by Django 2.0.4 on 2019-01-11 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_auto_20190110_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opencall',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.Transaction'),
        ),
    ]
