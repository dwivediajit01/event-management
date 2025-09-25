from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('manager/dashboard/', views.event_manager_dashboard, name='event_manager_dashboard'),
    path('event/', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('delete/<int:event_id>/', views.event_delete, name='event_delete'),
    path('register/<int:event_id>/', views.event_register, name='event_register'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/export/', views.export_event_csv, name='export_event_csv'),
    path('event/<int:event_id>/attendees/',views. view_event_attendees, name='view_event_attendees'),
    path('event/analytics/', views.event_analytics, name='event_analytics'),
    
    path('unregister/<int:event_id>/', views.unregister_event, name='unregister_event'),
    path('profile/', views.attendee_profile_view, name='attendee_profile'),


]
