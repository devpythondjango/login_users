# Generated by Django 4.2.5 on 2024-02-24 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_logincreate_application_login_create'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='group',
        ),
        migrations.RemoveField(
            model_name='application',
            name='image',
        ),
        migrations.RemoveField(
            model_name='application',
            name='kurs',
        ),
    ]