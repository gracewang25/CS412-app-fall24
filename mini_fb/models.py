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


    
class StatusMessage(models.Model):
    '''Models the data attributes of Facebook status message.'''
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f"{self.profile.first_name}: {self.message[:30]}"