from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):

    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to='user', null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




class Participant(models.Model):
    email=models.EmailField()
    name=models.CharField(max_length=200, null=True)
    phone=models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.email


class Speaker(models.Model):
    user=models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200, null=True, blank=True,)
    phone=models.CharField(max_length=200,null=True, blank=True)
    meetup_name=models.CharField(max_length=200,  null=True, blank=True)
    image=models.ImageField(upload_to='speaker_images')
    bio=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    
    

class Meetup(models.Model):
      title=models.CharField(max_length=500)
      description=models.TextField()
      user=models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null=True, blank=True)
      organizer_email=models.EmailField(max_length=254, null=True)
      slug=models.SlugField(unique=True)
      
      location_name=models.CharField(max_length=50,  null=True, blank=True)
      location_address=models.TextField( null=True, blank=True)
      participant=models.ManyToManyField(Participant, blank=True)
      meetup_speakers=models.ManyToManyField(Speaker )
      activate=models.BooleanField(default=True)
      created=models.DateTimeField(auto_now_add=True)
      meetup_date=models.DateField(blank=True, null=True)
      meetup_time=models.TimeField()
      from_date=models.DateField()
      to_date=models.DateField()
      image=models.ImageField(upload_to='images')

     
      def __str__(self):
        return f'{self.title}'
        


 