from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('book/<int:schedule_id>/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),

]
