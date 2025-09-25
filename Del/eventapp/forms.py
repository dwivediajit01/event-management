from django import forms
from .models import Event, Attendee

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'description', 'max_capacity']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = '__all__'

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Make profile photo input compatible with file upload
        self.fields['profile_photo'].widget.attrs['class'] = 'form-control-file'