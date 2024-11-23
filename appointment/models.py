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
    time = models.TimeField()  # TimeField for storing time
    floor = models.PositiveIntegerField()
    room_number = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        # Format time as AM/PM
        time_str = self.time.strftime('%I:%M %p')
        return f"{self.doctor.user.username} - {self.day} {time_str} (Room {self.room_number}, Floor {self.floor})"

    class Meta:
        unique_together = ('doctor', 'day', 'time')

