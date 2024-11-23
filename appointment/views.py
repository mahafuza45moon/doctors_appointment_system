from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Schedule, Appointment
from member.models import AppUser
from django.utils.timezone import now

# @login_required
def home(request):
    return render(request, 'appointment/home.html')

@login_required
def schedule_list(request):
    schedules = Schedule.objects.filter(active=True).order_by('day', 'time')
    return render(request, 'appointment/schedule_list.html', {'schedules': schedules})

@login_required
def book_appointment(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id, active=True)

    if request.method == 'POST':
        reason = request.POST.get('reason')

        from datetime import datetime, timedelta

        day_map = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6,
        }
        today = datetime.today()
        schedule_weekday = day_map[schedule.day.lower()]
        current_weekday = today.weekday()
        days_until_appointment = (schedule_weekday - current_weekday) % 7
        appointment_date = today + timedelta(days=days_until_appointment)

        if Appointment.objects.filter(schedule=schedule, patient=request.user.appuser).exists():
            return render(request, 'appointment/book_appointment.html', {
                'schedule': schedule,
                'error': "You already have an appointment for this schedule.",
            })

        Appointment.objects.create(
            patient=request.user.appuser,
            doctor=schedule.doctor,
            schedule=schedule,
            reason=reason,
        )
        return redirect('appointment_list')

    return render(request, 'appointment/book_appointment.html', {'schedule': schedule})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(patient=request.user.appuser)

    return render(request, 'appointment/appointment_list.html', {
        'appointments': appointments
    })
