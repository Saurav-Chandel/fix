# Generated by Django 4.0.2 on 2022-02-22 11:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_customermodel_date_join'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('arabic_name', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('selection_image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('options', models.CharField(max_length=500)),
                ('arabic_options', models.CharField(blank=True, max_length=500, null=True)),
                ('problem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.problems')),
            ],
        ),
        migrations.CreateModel(
            name='ArchivedCustomers',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='Customer', max_length=500)),
                ('email', models.EmailField(blank=True, max_length=70, null=True)),
                ('dob', models.DateField(blank=True, default=None, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('device_token', models.CharField(blank=True, max_length=500, null=True)),
                ('device_type', models.CharField(blank=True, max_length=7, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=7, null=True)),
                ('profile_images', models.ImageField(blank=True, null=True, upload_to='Customer_Profile_Images/')),
                ('date_joined', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('phone_otp', models.BigIntegerField(blank=True, null=True)),
                ('email_otp', models.BigIntegerField(blank=True, null=True)),
                ('is_mail_verified', models.BooleanField(default=False)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('total_points', models.BigIntegerField(default=0)),
                ('referal_code', models.CharField(blank=True, max_length=7, null=True)),
                ('invitation_code', models.CharField(blank=True, max_length=7, null=True)),
                ('type', models.CharField(blank=True, max_length=500, null=True)),
                ('language_id', models.CharField(blank=True, max_length=6, null=True)),
                ('active', models.CharField(default='Yes', max_length=100)),
                ('is_disabled', models.BooleanField(default=False)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
                ('delete_reason_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.reasons')),
            ],
        ),
    ]