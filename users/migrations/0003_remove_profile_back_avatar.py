# Generated by Django 4.2.6 on 2024-01-05 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_applicationcreate_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='back_avatar',
        ),
    ]