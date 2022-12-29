from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.
class CustomUser(AbstractUser):
    ''' Custom user to override the default user settings '''
    
    def get_absolute_url(self):
        return reverse('edit-user')

class Profile(models.Model):
    '''Model for the user profile with follows and followers'''
    user = models.OneToOneField(get_user_model(), primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE )
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile_pic/")
    bio = models.TextField(max_length=250, blank=True, null=True)
    followers = models.ManyToManyField(
        get_user_model(),
        related_name="following",
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

# signals for profile
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs): 
    if created:
        Profile.objects.create(user = instance)
    

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()