# Generated by Django 5.1.3 on 2024-11-23 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday')], max_length=10)),
                ('time', models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], max_length=2)),
                ('floor', models.PositiveIntegerField()),
                ('room_number', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(limit_choices_to={'user_type': 'doctor'}, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='member.appuser')),
            ],
            options={
                'unique_together': {('doctor', 'day', 'time')},
            },
        ),
    ]
