# Generated by Django 4.2.2 on 2023-08-24 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address2',
            field=models.TextField(default='man'),
        ),
        migrations.AddField(
            model_name='user',
            name='postal_code2',
            field=models.IntegerField(default='123'),
        ),
    ]
