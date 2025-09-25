from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from utils.decorators import role_required
from utils.session_helpers import ensure_role_in_session
from utils.event_time import get_upcoming_and_past_events
from .models import Event, Attendee
from .forms import EventForm, AttendeeForm


import csv

# -----------------------------
# 📌 Home Page
# -----------------------------
def home(request):
    ensure_role_in_session(request)   #To store the user data in session after login
    return render(request, 'home.html')


# -----------------------------
# 👥 Attendee Dashboard
# -----------------------------
@login_required
def event_list(request):
    # Redirect EventManagers to their own dashboard
    if request.session.get('role') == 'EventManager':
        return redirect('event_manager_dashboard')

    now = timezone.localtime()
    upcoming_events = Event.objects.filter(date__gte=now).order_by('date')
    past_events = Event.objects.filter(date__lt=now).order_by('-date')

    # Annotate upcoming events with remaining time (From the event_time.py)
    upcoming_events, past_events = get_upcoming_and_past_events()

    return render(request, 'eventapp/event_list.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })


# -----------------------------
# 🧑‍💼 Event Manager Dashboard
# -----------------------------
@role_required('EventManager')
def event_manager_dashboard(request):

    # Annotate upcoming events with remaining time (From the event_time.py)
    upcoming_events, past_events = get_upcoming_and_past_events()
    return render(request, 'eventapp/event_list.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })
    


# -----------------------------
# ➕ Create New Event
# -----------------------------
@role_required('EventManager')
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "✅ Event created successfully.")
        return redirect('event_manager_dashboard')
    return render(request, 'eventapp/event_form.html', {'form': form})


# -----------------------------
# ❌ Delete an Event
# -----------------------------
@role_required('EventManager')
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "✅ Event deleted successfully.")
        return redirect('event_manager_dashboard')
    return render(request, 'eventapp/event_confirm_delete.html', {'event': event})


# -----------------------------
# ✅ Register for Event
# -----------------------------
@role_required('Attendee')
def event_register(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # ✅ Prevent registering for past events
    if event.date <= timezone.localtime():
        messages.error(request, "⛔ Registration is closed. The event has already started.")
        return redirect('event_list')
    
    # ✅ Prevent duplicate registration
    if Attendee.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, "⚠️ You’ve already registered for this event.")
        return redirect('event_detail', event_id=event.id)


    # ✅ Prevent registration if the event is full
    if event.is_full():
        messages.warning(request, "⚠️ Sorry, this event is full.")
        return redirect('event_list')
    

    form = AttendeeForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        attendee = form.save(commit=False)
        attendee.event = event
        attendee.user = request.user  # ✅ Save logged-in user
        attendee.save()

        # Send confirmation email
        send_mail(
            'Event Registration Confirmed',
            f'Thank you {attendee.name} for registering for {event.title} on {event.date}.',
            settings.EMAIL_HOST_USER,
            [attendee.email],
            fail_silently=False,
        )

        messages.success(
            request,
            f"✅ Registered for {event.title}. Confirmation sent to {attendee.email}."
        )
        return redirect('event_list')

    return render(request, 'eventapp/register_form.html', {'form': form, 'event': event})


# -----------------------------
# 🔍 Event Detail
# -----------------------------
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = Attendee.objects.filter(event=event)
    return render(request, 'eventapp/event_detail.html', {
        'event': event,
        'attendees': attendees
    })


# -----------------------------
# 📤 Export Attendee List to CSV
# -----------------------------
@role_required('EventManager')
def export_event_csv(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = Attendee.objects.filter(event=event)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{event.title}_attendees.csv"'

    writer = csv.writer(response)
    writer.writerow(['Event Title', 'Event Date', 'Description'])
    writer.writerow([event.title, event.date, event.description])
    writer.writerow([])  # Blank line
    writer.writerow(['Name', 'Email'])
    writer.writerows([[a.name, a.email] for a in attendees])

    return response


#--------------------------------------
# 📋 View Attendees of a Specific Event
# ------------------------------------
@role_required('EventManager')
def view_event_attendees(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = Attendee.objects.filter(event=event).order_by('-registered_at')

    return render(request, 'eventapp/attendee_list.html', {
        'event': event,
        'attendees': attendees
    })

from django.db.models import Count

@role_required('EventManager')
def event_analytics(request):
    # Aggregate number of attendees per event
    event_data = (
        Event.objects.annotate(attendee_count=Count('attendee'))
        .values('title', 'attendee_count')
    )


#------------------------------
#📋  Prepare data for chart
#------------------------------
from django.db.models import Count
from django.db.models.functions import TruncDate


@role_required('EventManager')
def event_analytics(request):
    # Aggregate number of attendees per event
    event_data = (
        Event.objects.annotate(attendee_count=Count('attendee'))
        .values('title', 'attendee_count')
    )

    # Prepare data for Bar and pie  chart
    chart_data = [['Event Title', 'Attendees']]
    pie_data = [['Event', 'Attendees']]
    total_attendees = 0

    for item in event_data:
        chart_data.append([item['title'], item['attendee_count']])
        pie_data.append([item['title'], item['attendee_count']])
        total_attendees += item['attendee_count']

    total_events = event_data.count()
    avg_attendees = total_attendees / total_events if total_events > 0 else 0


    # 🔝 Top 5 Events
    top_events = (
        Event.objects.annotate(attendee_count=Count('attendee'))
        .order_by('-attendee_count')[:5]
        .values('title', 'attendee_count')
    )
    top_events_data = [['Event Title', 'Attendees']]
    for e in top_events:
        top_events_data.append([e['title'], e['attendee_count']])

    # 📉 Registration Trends Over Time
    registration_trend = (
        Attendee.objects.annotate(reg_date=TruncDate('registered_at'))
        .values('reg_date')
        .annotate(count=Count('id'))
        .order_by('reg_date')
    )
    trend_data = [['Date', 'Registrations']]
    for entry in registration_trend:
        trend_data.append([entry['reg_date'].strftime('%Y-%m-%d'), entry['count']])

    return render(request, 'eventapp/event_analytics.html', {
        'chart_data': chart_data,
        'pie_data': pie_data,
        'total_events': total_events,
        'total_attendees': total_attendees,
        'avg_attendees': round(avg_attendees, 2),
        'top_events_data': top_events_data,
        'trend_data': trend_data
    })


#-------------------------------
# 🤵‍♂️Attendes Profile
#--------------------------------
from .forms import AttendeeForm

@role_required('Attendee')
def attendee_profile_view(request):
    # Fetch the attendee profile linked to the user (any one, since profile is same for all events)
    attendee = Attendee.objects.filter(user=request.user).first()

    if not attendee:
        messages.warning(request, "Profile not found. Please register for an event to create your profile.")
        return redirect('event_list')

    
    else:
        form = AttendeeForm(instance=attendee)

 
    # Fetch all event registrations by this user
    my_registrations = Attendee.objects.filter(user=request.user).select_related('event').order_by('-registered_at')

    return render(request, 'eventapp/attendee_profile.html', {
        'attendee': attendee,
        'my_registrations': my_registrations,
        'now': timezone.now(),
    })
@role_required('Attendee')
def unregister_event(request, event_id):

    attendee = Attendee.objects.filter(user=request.user, event_id=event_id).first()

    if attendee:
        event = attendee.event   # ✅ Retrieve the event from the attendee
        attendee.delete()
        # Send email confirmation of unregistration
       
        send_mail(
            subject=f'Unregistered from {event.title}',
            message=(
                f'Hello {request.user.first_name or "Attendee"},\n\n'
                f'You have successfully unregistered from the event "{event.title}" '
                f'scheduled on {event.date.strftime("%B %d, %Y at %I:%M %p")}.\n\n'
                'We hope to see you at another event soon!\n\n'
                f'–  Team'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[attendee.email],
            fail_silently=False,
        )

        messages.success(request, 'You have successfully unregistered from the event.')
    else:
        messages.error(request, 'You are not registered for this event.')
    return redirect('attendee_profile')


