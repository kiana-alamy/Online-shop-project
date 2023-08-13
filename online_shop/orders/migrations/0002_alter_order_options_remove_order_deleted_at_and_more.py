# Generated by Django 4.2.2 on 2023-08-13 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('paid', '-updated')},
        ),
        migrations.RemoveField(
            model_name='order',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='order',
            name='description',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='order',
            name='offer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='restored_at',
        ),
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='created',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='restored_at',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='updated',
        ),
    ]