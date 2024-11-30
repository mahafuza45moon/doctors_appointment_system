from django.db import models
from member.models import AppUser

class Schedule(models.Model):
    WEEK_DAYS = [
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
    ]

    doctor = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': AppUser.DOCTOR},
        related_name='schedules'
    )
    day = models.CharField(max_length=10, choices=WEEK_DAYS)
    time = models.TimeField()
    floor = models.PositiveIntegerField()
    room_number = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        # Format time as AM/PM
        time_str = self.time.strftime('%I:%M %p')
        return f"{self.doctor.user.username} - {self.day} {time_str} (Room {self.room_number}, Floor {self.floor})"

    class Meta:
        unique_together = ('doctor', 'day', 'time')

class Appointment(models.Model):
    patient = models.ForeignKey(AppUser, on_delete=models.CASCADE, limit_choices_to={'user_type': AppUser.PATIENT}, related_name='appointments_as_patient')
    doctor = models.ForeignKey(AppUser, on_delete=models.CASCADE, limit_choices_to={'user_type': AppUser.DOCTOR}, related_name='appointments_as_doctor')
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='appointments')
    reason = models.TextField(max_length=500, blank=True, null=True)
    file_upload = models.FileField(upload_to='uploads/documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.username} on {self.get_appointment_datetime()}"

    def get_appointment_datetime(self):
        from datetime import datetime, timedelta
        day_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
        }
        today = datetime.today()
        schedule_weekday = day_map[self.schedule.day.lower()]
        current_weekday = today.weekday()
        days_until_appointment = (schedule_weekday - current_weekday) % 7
        appointment_date = today + timedelta(days=days_until_appointment)
        return datetime.combine(appointment_date.date(), self.schedule.time)