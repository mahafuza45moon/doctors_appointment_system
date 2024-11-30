from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Schedule, Appointment
from member.models import AppUser
from django.utils.timezone import now
from django.contrib import messages


# @login_required
def home(request):
    return render(request, 'appointment/home.html')

@login_required
def cancel_appointment(request, appointment_id):
    # Get the appointment using the appointment ID
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if the logged-in user is the patient who owns the appointment
    if appointment.patient != request.user.appuser:
        messages.error(request, "You are not authorized to cancel this appointment.")
        return redirect('appointment_list')

    # Delete the appointment if it's the patient's appointment
    appointment.delete()

    # Add a success message
    messages.success(request, "Your appointment has been canceled successfully.")

    # Redirect to the appointment list page
    return redirect('appointment_list')

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure the user is the patient of the appointment
    if appointment.patient != request.user.appuser:
        messages.error(request, "You are not authorized to edit this appointment.")
        return redirect('appointment_list')

    if request.method == 'POST':
        reason = request.POST.get('reason')
        file_upload = request.FILES.get('file_upload')
        schedule_id = request.POST.get('schedule_id')

        # Update reason and file upload if provided
        appointment.reason = reason
        if file_upload:
            appointment.file_upload = file_upload

        # Update the schedule if provided
        if schedule_id and schedule_id != str(appointment.schedule.id):
            new_schedule = get_object_or_404(Schedule, id=schedule_id)
            appointment.schedule = new_schedule

        appointment.save()
        messages.success(request, "Your appointment has been updated successfully.")
        return redirect('appointment_list')

    # Get all schedules for the current doctor
    available_schedules = Schedule.objects.filter(
        doctor=appointment.doctor,
        active=True
    ).exclude(appointments__patient=appointment.patient)

    return render(request, 'appointment/edit_appointment.html', {
        'appointment': appointment,
        'available_schedules': available_schedules
    })

@login_required
def schedule_list(request):
    if request.user.appuser.user_type == 'doctor':
        schedules = Schedule.objects.filter(doctor=request.user.appuser, active=True).order_by('day', 'time')
        return render(request, 'appointment/doctor_schedule_list.html', {'schedules': schedules})
    else:
        # Fetch all active schedules for patients
        schedules = Schedule.objects.filter(active=True).order_by('day', 'time')
        return render(request, 'appointment/patient_schedule_list.html', {'schedules': schedules})

@login_required
def appointment_detail(request, appointment_id):
    # Ensure the user is a doctor
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.appuser)

    return render(request, 'appointment/appointment_detail.html', {'appointment': appointment})

@login_required
def book_appointment(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id, active=True)

    if request.user.appuser == schedule.doctor:
        return render(request, 'appointment/book_appointment.html', {
            'schedule': schedule,
            'error': "You cannot book an appointment with yourself.",
        })

    if request.method == 'POST':
        reason = request.POST.get('reason')
        file_upload = request.FILES.get('file_upload')

        # Check if patient already has an appointment for this schedule
        if Appointment.objects.filter(schedule=schedule, patient=request.user.appuser).exists():
            return render(request, 'appointment/book_appointment.html', {
                'schedule': schedule,
                'error': "You already have an appointment for this schedule.",
            })

        # Create the appointment
        Appointment.objects.create(
            patient=request.user.appuser,
            doctor=schedule.doctor,
            schedule=schedule,
            reason=reason,
            file_upload=file_upload  # Save the uploaded file
        )

        # Add success message after creating the appointment
        messages.success(request, 'Your appointment has been successfully booked!')

        # Redirect to the appointment list page
        return redirect('appointment_list')

    return render(request, 'appointment/book_appointment.html', {'schedule': schedule})


@login_required
def appointment_list(request):
    if request.user.appuser.user_type == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user.appuser)
        template_name = 'appointment/doctor_appointment_list.html'
    else:
        appointments = Appointment.objects.filter(patient=request.user.appuser)
        template_name = 'appointment/patient_appointment_list.html'

    return render(request, template_name, {'appointments': appointments})
