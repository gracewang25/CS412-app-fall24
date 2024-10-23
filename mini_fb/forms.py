# File: mini_fb/models.py
# Author: Grace Wang (grace25@bu.edu), 10/14/2024
# Description: This file defines the Create Profile form to allow users to input their oown profiles.
from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''Form to create a new StatusMessage with optional images.'''
    class Meta:
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    '''Form to update a Profile.'''
    class Meta:
        model = Profile
        fields = ['email_address', 'city', 'profile_image_url']
