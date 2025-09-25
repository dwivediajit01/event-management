#To ensure the navbar visible in the home page (As after login the session cleared the user login data)


from django.contrib.auth.models import Group

def ensure_role_in_session(request):
    if request.user.is_authenticated and 'role' not in request.session:
        groups = request.user.groups.values_list('name', flat=True)
        if 'EventManager' in groups:
            request.session['role'] = 'EventManager'
        elif 'Attendee' in groups:
            request.session['role'] = 'Attendee'
