from eventapp.models import Event
from django.utils import timezone

def get_upcoming_and_past_events():
    now = timezone.localtime()
    upcoming_events = []
    past_events = []

    for event in Event.objects.all().order_by('-date'):
        if event.date >= now:
            delta = event.date - now
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes = remainder // 60

            if days > 0:
                event.time_left = f"{days} day(s), {hours} hour(s)"
            elif hours > 0:
                event.time_left = f"{hours} hour(s), {minutes} min(s)"
            else:
                event.time_left = f"{minutes} min(s)"
            upcoming_events.append(event)
        else:
            past_events.append(event)

    return upcoming_events, past_events
