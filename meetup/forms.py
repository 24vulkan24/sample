from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Meetup, CustomUser,Participant,Speaker
from django.forms import Textarea, TextInput, PasswordInput, CheckboxInput, FileInput
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django .conf import settings
from django .core.mail import send_mail
class MeetupForm(forms.ModelForm):
    class Meta:
        model = Meetup
        fields ='__all__'
        exclude=['slug','user','participant', 'meetup_speakers']
        widgets = {
            'meetup_date' : DatePickerInput(
                attrs={
                  
                   "class":"form-control"
                   
                }
            ),
            'from_date' : DatePickerInput(
                attrs={
                  
                   "class":"form-control"
                   
                }
            ),
            'to_date' : DatePickerInput(
                attrs={
                  
                   "class":"form-control"
                   
                }
            ),
            'meetup_time':TimePickerInput(
                attrs={
                  
                   "class":"form-control"
                   
                }
            ),
            'location_address':Textarea(
                attrs={
                    "placeholder": "Enter location address"
                }
            ),
            'activate':CheckboxInput(
                attrs={
                    "class": "form-check form-switch",
                     "id":"mySwitch",

                }
            ), 
            'description':Textarea(
                
                attrs={
                    
                    "class":"form-control"
                }
            ), 
            'title':TextInput(
                attrs={
              
                   "class":"form-control"
                   
                }
            ),
            
            'organizer_email':TextInput(
                attrs={
                   
                   "class":"form-control"
                }
            ),
            'location_address':Textarea(
                attrs={
                   
                   "class":"form-control"
                }
            ),

             'location_name':TextInput(
                attrs={
               
                   "class":"form-control"
                }
            ), 
             'image':FileInput(
                attrs={
              
                   "class":"form-control"
                   
                }
            ),
           
        }
      

class MyUserRegistrationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields= ['name', 'email', 'password1', 'password2']
        widgets = {
            
            
            'name':TextInput(
                attrs={
                   "placeholder": "Enter name",
                   "class":"form-control"
                }
            ),
            'email':TextInput(
                attrs={
                   "placeholder": "Enter email",
                   "class":"form-control"
                }
            ),
            'username':TextInput(
                attrs={
                   "placeholder": "Enter username",
                   "class":"form-control"
                }
            ),
            'phone':TextInput(
                attrs={
                   "placeholder": "Enter phone",
                   "class":"form-control"
                }
            ),
            
         }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields='__all__'
        widgets = {
            
            
            'name':TextInput(
                attrs={
                   "placeholder": "Enter name",
                   "class":"form-control"
                }
            ),
            'email':TextInput(
                attrs={
                   "placeholder": "Enter email",
                   "class":"form-control"
                }
            ),
           
            'phone':TextInput(
                attrs={
                   "placeholder": "Enter phone",
                   "class":"form-control"
                }
            ),
            
         }
class SpeakerForm(forms.ModelForm):
    class Meta:
        model=Speaker
        fields='__all__'
        exclude=['user']
        widgets = {
            
            
            'name':TextInput(
                attrs={
                   "placeholder": "Enter name",
                   "class":"form-control"
                }
            ),
            'email':TextInput(
                attrs={
                   "placeholder": "Enter email",
                   "class":"form-control"
                }
            ),
            'user':TextInput(
                attrs={
                   "placeholder": "Enter username",
                   "class":"form-control"
                }
            ),
            'phone':TextInput(
                attrs={
                   "placeholder": "Enter phone",
                   "class":"form-control"
                }
            ),
            'meetup_name':TextInput(
                attrs={
                    "placeholder":"Enter Meetup Name",
                    "class": "formcontrol"
                }
            ),

             'image':FileInput(
                attrs={
              
                   "class":"form-control"
                   
                }
            ),
            'bio':Textarea(
                attrs={"placeholder":"Write About Your Self (*_*)",
                "class":"form-control"}
            )
            
         }
        
class ContactForm(forms.Form):
    name= forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': '*Your Full Name..'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '*Your email..'})  )
    subject=forms.CharField(max_length=250,widget=forms.TextInput(attrs={'placeholder': '*Your subject..'}))
    phone=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': '*Your Phone No...', }))
    message= forms.CharField(widget=forms.Textarea(attrs={'placeholder': '*Your Message..'}))


    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('subject')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg

    def send(self):

        subject, msg = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )