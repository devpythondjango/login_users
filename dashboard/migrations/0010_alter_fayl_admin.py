# Generated by Django 4.2.6 on 2024-02-09 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_fayl_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fayl',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.adminprofile'),
        ),
    ]