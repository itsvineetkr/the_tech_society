# Generated by Django 5.1 on 2024-09-10 09:01

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('name', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('rollno', models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999999999999), django.core.validators.MinValueValidator(1000000000000)])),
                ('branch', models.CharField(choices=[('CSE', 'CSE Regular'), ('CSEAI', 'CSE AI'), ('CSESF', 'CSE SF'), ('ECE', 'Electronics'), ('EE', 'Electrical'), ('MEC', 'Mechanical'), ('CVL', 'Civil'), ('CHE', 'Chemical'), ('ADMIN', 'AdminUser')], max_length=5)),
                ('year', models.CharField(choices=[('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year'), ('ADMIN', 'AdminUser')], max_length=5)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
