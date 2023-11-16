from django.contrib import admin
from .models import Meetup,Participant, CustomUser, Speaker



# Register your models here.
class MeetupAdmin (admin.ModelAdmin):
   list_display=('title', 'organizer_email', 'location_name', )
   list_filter=('title',)
   prepopulated_fields={'slug':('title',)}
admin.site.register(Meetup, MeetupAdmin)
admin.site.register(Participant)
admin.site.register(CustomUser)
admin.site.register(Speaker)
