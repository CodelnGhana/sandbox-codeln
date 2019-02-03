# Generated by Django 2.0.4 on 2019-02-03 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('job_role', models.CharField(choices=[('full_stack_developer', 'Full Stack Developer'), ('frontend_developer', 'Frontend Developer'), ('backend_developer', 'Backend  Developer'), ('android_developer', 'Android  Developer'), ('graphic_designer', 'Graphic Designer'), ('ios_developer', 'IOS Developer'), ('data_scientist', 'Data Scientist')], default='full_stack_developer', max_length=30)),
                ('dev_experience', models.CharField(choices=[('entry', 'Entry'), ('junior', 'Junior'), ('mid-level', 'Mid-Level'), ('senior', 'Senior')], default='mid-level', max_length=30)),
                ('engagement_type', models.CharField(choices=[('full_time', 'Full-time'), ('part_time', 'Part-time'), ('contract', 'Contract'), ('remote', 'Remote'), ('freelance', 'Freelance')], default='full_time', max_length=30)),
                ('tech_stack', models.CharField(max_length=500)),
                ('num_devs_wanted', models.IntegerField(default=1)),
                ('remuneration_in_dollars', models.CharField(help_text='in dollars ($)', max_length=45)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_filled', models.BooleanField(default=False)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_statistics', to='marketplace.Job')),
            ],
            options={
                'ordering': ('position_filled',),
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d')),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female')], max_length=30, null=True)),
                ('phone_number', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='marketplace.Person')),
                ('linkedin_url', models.CharField(max_length=500, null=True)),
                ('portfolio', models.CharField(blank=True, max_length=500, null=True)),
                ('github_repo', models.CharField(max_length=500, null=True)),
                ('language', models.CharField(blank=True, max_length=140, null=True)),
                ('framework', models.CharField(blank=True, max_length=140, null=True)),
                ('years', models.CharField(choices=[('1-2', '1-2'), ('2-4', '2-4'), ('4-above', '4-above')], max_length=30, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('availability', models.CharField(choices=[('full_time', 'Full-time'), ('part_time', 'Part-time'), ('contract', 'Contract'), ('remote', 'Remote'), ('freelance', 'Freelance')], max_length=30, null=True)),
            ],
            bases=('marketplace.person',),
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='marketplace.Person')),
                ('company', models.CharField(blank=True, max_length=140, null=True)),
                ('job_role', models.CharField(blank=True, max_length=140, null=True)),
                ('industry', models.CharField(blank=True, max_length=80, null=True)),
                ('company_url', models.CharField(blank=True, max_length=500, null=True)),
            ],
            bases=('marketplace.person',),
        ),
        migrations.AddField(
            model_name='person',
            name='auth_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobstatistic',
            name='applied_by',
            field=models.ManyToManyField(related_name='applied_jobs', to='marketplace.Developer'),
        ),
        migrations.AddField(
            model_name='jobstatistic',
            name='recommended_devs',
            field=models.ManyToManyField(related_name='recommended_jobs', to='marketplace.Developer'),
        ),
        migrations.AddField(
            model_name='jobstatistic',
            name='selected_devs',
            field=models.ManyToManyField(related_name='jobs_picked_for', to='marketplace.Developer'),
        ),
        migrations.AddField(
            model_name='job',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_jobs', to='marketplace.Recruiter'),
        ),
    ]
