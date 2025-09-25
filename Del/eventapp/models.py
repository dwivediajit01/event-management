from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField()
    max_capacity = models.PositiveIntegerField(null=True, blank=True)  

    def seats_left(self):
        return self.max_capacity - self.attendee_set.count()

    def is_full(self):
        return self.max_capacity is not None and self.attendee_set.count() >= self.max_capacity

    def __str__(self):
        return self.title

class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True,null=True)

    # Profile enhancement fields
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"
