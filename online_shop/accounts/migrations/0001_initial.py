# Generated by Django 4.2.2 on 2023-08-01 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, help_text='This is deleted datetime', null=True, verbose_name='Deleted Datetime')),
                ('restored_at', models.DateTimeField(blank=True, editable=False, help_text='This is Restored Datetime', null=True, verbose_name='Restored Datetime')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, editable=False, help_text='This is deleted status', verbose_name='Deleted status')),
                ('is_active', models.BooleanField(default=True, editable=False, help_text='This is active status', verbose_name='Active status')),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('code', models.PositiveSmallIntegerField()),
                ('create', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, help_text='This is deleted datetime', null=True, verbose_name='Deleted Datetime')),
                ('restored_at', models.DateTimeField(blank=True, editable=False, help_text='This is Restored Datetime', null=True, verbose_name='Restored Datetime')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, editable=False, help_text='This is deleted status', verbose_name='Deleted status')),
                ('is_active', models.BooleanField(default=True, editable=False, help_text='This is active status', verbose_name='Active status')),
                ('address', models.CharField(max_length=200)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
