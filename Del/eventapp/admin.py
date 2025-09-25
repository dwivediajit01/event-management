from django.contrib import admin
from .models import Event,Attendee
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display=['id','title','date','description']

class AttendeAdmin(admin.ModelAdmin):
    list_display=['id','name','email','event']

admin.site.register(Event,EventAdmin)
admin.site.register(Attendee,AttendeAdmin)