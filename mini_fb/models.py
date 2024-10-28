# File: mini_fb/models.py
# Author: Grace Wang (grace25@bu.edu), 10/7/2024
# Description: This file defines the Profile model, representing Facebook 
# user profile data including first name, last name, city, email, and profile image URL.

from django.db import models
from django.utils import timezone
import pytz

# Create your models here.
class Profile(models.Model):
    '''Profile class for each unique user.'''

    # data attributes:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)

    published = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile.'''
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        # Convert timestamps to EST (Eastern Standard Time)
        est_tz = pytz.timezone('America/New_York')
        status_messages = self.status_messages.order_by('-timestamp')
        for status in status_messages:
            status.timestamp = status.timestamp.astimezone(est_tz)
        return status_messages
    
    def get_friends(self):
        friends1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        return Profile.objects.filter(id__in=list(friends1) + list(friends2))
    
    def add_friend(self, other):
            """Adds a friend if not already friends and not self-friending."""
            if self == other:
                return  # Prevent self-friending
            if not Friend.objects.filter(models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)).exists():
                Friend.objects.create(profile1=self, profile2=other, timestamp=timezone.now())

    def get_friend_suggestions(self):
            """Returns a list of profiles not friends with self and excludes self."""
            current_friends = self.get_friends().values_list('id', flat=True)
            return Profile.objects.exclude(id__in=current_friends).exclude(id=self.id)

    def get_news_feed(self):
        """Return a queryset of status messages from the profile and its friends, ordered by the most recent."""
        # Get friends' profiles
        friends_profiles = list(self.get_friends())
        
        # Include the profile itself and all friends
        profiles_to_include = [self] + friends_profiles
        
        # Get status messages for all profiles in profiles_to_include
        return StatusMessage.objects.filter(profile__in=profiles_to_include).order_by('-timestamp')




    
class StatusMessage(models.Model):
    '''Models the data attributes of Facebook status message.'''
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f"{self.profile.first_name}: {self.message[:30]}"
    
    def get_images(self):
        return Image.objects.filter(status_message=self)

class Image(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='status_images/')
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Image for status {self.status_message.id} uploaded on {self.timestamp}"

# File: mini_fb/models.py
# Author: Grace Wang (grace25@bu.edu), 10/7/2024
# Description: Defines the Friend model and Profile methods for managing friends.

class Friend(models.Model):
    profile1 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1.first_name} & {self.profile2.first_name}"

