# authapp/views.py
from django.contrib.auth.models import Group, User
from .forms import SignupForm
from django.contrib import messages
from django.shortcuts import render,redirect

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm

def signup_view(request):
    form=SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.save()

            # ✅ Automatically assign 'Attendee' role (no selection needed)
            attendee_group = Group.objects.get(name='Attendee')
            user.groups.add(attendee_group)

            messages.success(request, '✅ Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})



#Log in view
from .forms import LoginForm 
from django.contrib.auth import authenticate, login,logout




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            identifier = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=identifier, password=password)

            if user is None:
                try:
                    user_obj = User.objects.get(email=identifier)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user:
                # ✅ Check if user belongs to selected role
                if user.groups.filter(name=role).exists():
                    login(request, user)
                    request.session['role'] = role  # save role in   session

                    if role == 'EventManager':
                        return redirect('event_list')
                    else:
                        return redirect('event_list')
                else:
                    messages.error(request, f"You are not registered as a {role}.")
                    return render(request, 'accounts/login.html', {'form': form}) 
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, 'accounts/login.html', {'form': form}) 
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


#For logout
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('login')