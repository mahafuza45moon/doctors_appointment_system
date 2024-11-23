from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day', 'formatted_time', 'floor', 'room_number', 'active')
    list_filter = ('day', 'active')
    search_fields = ('doctor__user__email', 'floor', 'room_number')

    def formatted_time(self, obj):
        return obj.time.strftime('%I:%M %p')  # Display time as AM/PM
    formatted_time.short_description = 'Time'
