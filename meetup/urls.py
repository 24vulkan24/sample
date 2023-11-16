from django.urls import path
from . import views
from .views import MeetupUpdate, MeetupsCreate, MeetupDelete,SpeakerUpdate,\
     SpeakerDelete,SpeakerCreate,ParticipantDelete, Password_Reset_Complete,\
   AddParticipant,ParticipantUpdate, Password_Reset, Password_Reset_Done, Password_Reset_Confirm, Contact
from django.contrib.auth.views import LogoutView


urlpatterns = [
    
   path('', views.index, name='index' ),
   path('password-reset/', Password_Reset.as_view(), name='password-reset'),
   path('password-reset-complete/', Password_Reset_Complete.as_view(), name='password_reset_complete'),
   path('password-reset/done/', Password_Reset_Done.as_view(), name='password_reset_done'),
   path('password-reset-confirm/<uidb64>/<token>', Password_Reset_Confirm.as_view(), name='password_reset_confirm'),
   path('login/', views.LoginPage, name='login' ),
   path('register/', views.Register, name='register' ),
   path('user-meetups/', views.user_meetups, name='user-meetups' ),
   path('user-speakers/', views.user_speakers, name='user-speakers' ),
   path('meetup-speakers/<slug:slug>', views.meetup_speakers, name='meetup-speakers' ),
   path('meetup-participants/<slug:slug>', views.meetup_participants , name='meetup-participants' ),
   path('comfirm-registration/', views.comfirm_registration, name='comfirm-registration' ),
   path('meetup-details/<slug:meetup_slug>', views.meetup_details, name='meetup-details' ),
   path('speaker-details/<int:id>', views.speaker_details, name='speaker-details'),
   path('participant-details/<int:id>', views.participant_details, name='participant-details'),
   path('meetup-update/<int:pk>', MeetupUpdate.as_view(), name='meetup-update'),
   path('speaker-update/<int:pk>', SpeakerUpdate.as_view(), name='speaker-update'),
   path('participant-update/<int:pk>',ParticipantUpdate.as_view(), name='participant-update'),
   path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
   path('meetup-create/', MeetupsCreate.as_view(), name='meetup-create'),
   path('speaker-create/', SpeakerCreate.as_view(), name='speaker-create'),
   #path('participant-add/', AddParticipant.as_view(), name='participant-add'),
   path('participant-add/<slug:meetup_slug>', views.addParticipant, name='participant-add'),
   path('meetup-delete/<int:pk>', MeetupDelete.as_view(), name='meetup-delete'),
   path('speaker-delete/<int:pk>', SpeakerDelete.as_view(), name='speaker-delete'),
   path('participant-delete/<int:pk>', ParticipantDelete.as_view(), name='participant-delete'),
   path('contact/', Contact.as_view(), name='contact'),
   # path('contact/', views.contact, name='contact'),
   path('contact-success/', views.contact_success, name='contact-success'),
]

