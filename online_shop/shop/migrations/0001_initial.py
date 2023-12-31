# Generated by Django 4.2.2 on 2023-08-03 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('is_sub', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='shop.category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'caregories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, help_text='This is deleted datetime', null=True, verbose_name='Deleted Datetime')),
                ('restored_at', models.DateTimeField(blank=True, editable=False, help_text='This is Restored Datetime', null=True, verbose_name='Restored Datetime')),
                ('is_deleted', models.BooleanField(db_index=True, default=False, editable=False, help_text='This is deleted status', verbose_name='Deleted status')),
                ('is_active', models.BooleanField(default=True, editable=False, help_text='This is active status', verbose_name='Active status')),
                ('image', models.ImageField(upload_to='products/%Y/%m/%d')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('quantity', models.PositiveIntegerField()),
                ('count_buying', models.PositiveIntegerField()),
                ('rate', models.PositiveIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='shop.category')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
    ]
