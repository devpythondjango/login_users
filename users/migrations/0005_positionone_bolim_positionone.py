# Generated by Django 4.2.6 on 2023-10-16 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_teacher_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PositionOne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=70, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='bolim',
            name='positionone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.positionone'),
        ),
    ]