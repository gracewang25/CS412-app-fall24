# File: mini_fb/models.py
# Author: Grace Wang (grace25@bu.edu), 10/7/2024
# Description: This file defines the Profile model, representing Facebook 
# user profile data including first name, last name, city, email, and profile image URL.

from django.db import models

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
    