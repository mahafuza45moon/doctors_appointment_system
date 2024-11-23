from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('book/<int:schedule_id>/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
]
