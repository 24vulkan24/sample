from django.shortcuts import render, redirect
from . models import Meetup, Speaker,Participant
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.views.generic.edit import  UpdateView, CreateView, DeleteView, FormView
from . forms import MeetupForm, MyUserRegistrationForm, ParticipantForm, SpeakerForm, ContactForm
from string import punctuation
from random import choice, randint
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
# from django.core.mail import send_mail
# from django.conf import settings

# Create your views here.
#FBV

#Login 

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=='POST':
        email=request.POST.get('email')
        email.lower()
        password=request.POST.get('password')
        user=authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')


    return render(request, 'meetup/login.html')
#Registrtation

def Register(request):
    form=MyUserRegistrationForm()

    context={'form':form}
    if request.method=='POST':
        form=MyUserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
    return render(request, 'meetup/register.html', context)


def index(request):
    title='Meetups'
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
  
    meetups=Meetup.objects.filter(activate=True)
    meetups=meetups.filter(
        
        Q(title__icontains=q)|
        Q(location_name__icontains=q)|
        Q(from_date__icontains=q)|
        Q(to_date__icontains=q)
        ) 
    
    return render(request, 'meetup/index.html', {'title':title, 'meetups':meetups})

def meetup_details(request, meetup_slug):
    try:

        meetup=Meetup.objects.get(slug=meetup_slug)
        speakers=Speaker.objects.filter(user=meetup.user)
        if request.method=="GET":
            participantForm=ParticipantForm()
        else:
             participantForm=ParticipantForm(request.POST)
             if participantForm.is_valid():
                 participant=participantForm.save()
                 meetup.participant.add(participant)
                 return redirect('comfirm-registration')
        
    except Exception as exc:
       pass
    return render(request, 'meetup/meetup_details.html', {'meetup':meetup, 'form':participantForm, 'speakers':speakers})

#User Meetups
def user_meetups(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    meetups=Meetup.objects.filter(user=request.user.id)
   
    meetups=meetups.filter(
        
        Q(title__icontains=q)|
        Q(location_name__icontains=q)|
        Q(from_date__icontains=q)|
        Q(to_date__icontains=q)
        ) 
    
    return render(request, 'meetup/user_meetups.html', { 'meetups':meetups})





#CBV Class Based 
#Update Meetups
class MeetupUpdate(UpdateView):
    model=Meetup
    form_class = MeetupForm
    template_name='meetup/meetup_form.html'
    success_url=reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(MeetupUpdate, self).form_valid(form)
    

#add meetups class
class MeetupsCreate(CreateView):
    model=Meetup
    form_class = MeetupForm
    #exclude=[]
    success_url=reverse_lazy('index')
    template_name='meetup/meetup_form.html'
    def form_valid(self, form):
        form.instance.user=self.request.user
        for i in punctuation:
            title=form.instance.title.replace(i, ' ')
        s=randint(100,1000)
        title=title+'-'+str(s)
        form.instance.slug=title.replace(' ', '-')
        return super(MeetupsCreate, self).form_valid(form)


#Meetup Delete

#Delete Meetups
class MeetupDelete(DeleteView):
    model=Meetup
    context_object_name='meetup'
    template_name='meetup/delete_meetup.html'
    success_url=reverse_lazy('index')

#Comfirmation page

def comfirm_registration(request):
    return render(request, 'meetup/registration_comfrim.html')


#speakers
def meetup_speakers(request, slug):
    meetup=Meetup.objects.get(slug=slug)
    speakers=meetup.meetup_speakers.all
    return render(request, 'meetup/meetup_speakers.html', {'speakers':speakers, 'meetup':meetup})

# def speaker_details(request,email):
#     speakers=Speaker.objects.get(email=email)
#     return render(request, 'meetup/speaker_details.html',{'speakers': speakers, })

def speaker_details(request,id):
    speakers=Speaker.objects.get(id=id)
    return render(request, 'meetup/speaker_details.html',{'speakers': speakers, })

class SpeakerUpdate(UpdateView):
    model=Speaker
    form_class = SpeakerForm
    template_name='meetup/speaker_form.html'
    success_url=reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(SpeakerUpdate, self).form_valid(form)

class SpeakerDelete(DeleteView):
    model=Speaker
    context_object_name='speaker'
    template_name='meetup/delete_speaker.html'
    success_url=reverse_lazy('index')

class SpeakerCreate(CreateView):
    model=Speaker
    form_class = SpeakerForm
    #exclude=[]
    success_url=reverse_lazy('index')
    template_name='meetup/Speaker_add.html'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(SpeakerCreate, self).form_valid(form)



# def contact(request):
#     if request.method=='POST':
#         form=ContactForm(request.POST)
#         if form.is_valid():
#             clear_data=form.super().clean()
#             clear_data.get('name')
#             # name=form.get('name')
#             # email=form.get('email')
#             # phone=form.get('phone')
#             # subject=form.get('subject')
#             # message=form.get('message')
#             # msg=f'{name} with {email} and {phone}'
#             # msg+=f'\n "{subject}"\n\n'
#             # msg+=message
            


#             print('Form was valid')
#             #send_mail(subject=subject, message=msg, from_email=settings.EMAIL_HOST_USER,recipient_list=settings.recipient_address )
#             send_mail(subject='hello', message='Just testing', from_email=settings.EMAIL_HOST_USER, recipient_list=['hayatudeenisah92@gmail.com'] )
#             return redirect('contact-success')
            
#     else:
#         form=ContactForm()
#     return render(request, 'meetup/contact.html',{'form':form})

def meetup_participants(request, slug):
    meetup=Meetup.objects.get(slug=slug)
    participants=meetup.participant.all
    return render(request, 'meetup/meetup_participants.html', {'participants':participants, 'meetup':meetup})

def participant_details(request,id):
    participants=Participant.objects.get(id=id)
    return render(request, 'meetup/participant_details.html',{'participants':participants, })

#
def addParticipant(request, meetup_slug):
    meetup=Meetup.objects.get(slug=meetup_slug)
    if request.method=="GET":
        participantForm=ParticipantForm()
    else:
          participantForm=ParticipantForm(request.POST)
          if participantForm.is_valid():
              participant=participantForm.save()
              meetup.participant.add(participant)
              return redirect('meetup-participants', meetup_slug)
    context={'meetup':meetup, 'form':participantForm}

    return render(request, 'meetup/Participant_form.html', context)

class ParticipantDelete(DeleteView):
    model=Participant
    context_object_name='participant'
    template_name='meetup/delete_participant.html'
    success_url=reverse_lazy('index')

class AddParticipant(CreateView):
    model=Participant
    form_class = ParticipantForm
    #exclude=[]
    success_url=reverse_lazy('index')
    template_name='meetup/Participant_form.html'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(AddParticipant, self).form_valid(form)
    
class ParticipantUpdate(UpdateView):
    model=Participant
    form_class = ParticipantForm
    template_name='meetup/Participant_update.html'
    success_url=reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(ParticipantUpdate, self).form_valid(form)
    
def contact_success(request):
    return render(request, 'meetup/contact_success.html')

def user_speakers(request):
   
    speakers=Speaker.objects.filter(user=request.user.id)
   
    # meetups=meetups.filter(
        
    #     Q(title__icontains=q)|
    #     Q(location_name__icontains=q)|
    #     Q(from_date__icontains=q)|
    #     Q(to_date__icontains=q)
    #     ) 
    
    return render(request, 'meetup/user_speakers.html', { 'speakers':speakers})

#Forget Password
class Password_Reset(PasswordResetView):
    template_name='user/password_reset_form.html'


class Password_Reset_Done(PasswordResetDoneView):
    template_name='user/password_reset_done_form.html'

class Password_Reset_Confirm(PasswordResetConfirmView):
    template_name='user/password_reset_confirm_form.html'

class Password_Reset_Complete(PasswordResetCompleteView):
    template_name='user/password_reset_complete.html'






class Contact(FormView):
    template_name = 'meetup/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact-success')

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)



# def deleteMeetup(request, id):
#     meetup=Meetup.objects.get(pk=id)
#     meetup.delete()

#     return render(request, 'meetup-delete')


