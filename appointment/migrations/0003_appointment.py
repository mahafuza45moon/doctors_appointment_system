# Generated by Django 5.1.3 on 2024-11-23 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_alter_schedule_time'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(limit_choices_to={'user_type': 'doctor'}, on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_doctor', to='member.appuser')),
                ('patient', models.ForeignKey(limit_choices_to={'user_type': 'patient'}, on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_patient', to='member.appuser')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='appointment.schedule')),
            ],
        ),
    ]
