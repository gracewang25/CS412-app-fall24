# File: mini_fb/views.py
# Author: Grace Wang (grace25@bu.edu), 10/7/2024
# Description: This file contains the Django class-based views for 
# the mini Facebook application. It includes the ShowAllProfilesView, 
# which displays all profiles.

from django.shortcuts import render
from .models import *
from django.views.generic import ListView

# Create your views here.

# class-based view
class ShowAllProfilesView(ListView):
    '''A view to show all Profiles.'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
