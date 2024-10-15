# File: mini_fb/views.py
# Author: Grace Wang (grace25@bu.edu), 10/7/2024
# Description: This file contains the Django class-based views for 
# the mini Facebook application. It includes the ShowAllProfilesView, 
# which displays all profiles.

from django.shortcuts import render
from .models import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django import forms
from .models import Profile
from django.urls import reverse
from django.views.generic import CreateView
from .forms import *


# Create your views here.

# class-based view
class ShowAllProfilesView(ListView):
    '''A view to show all Profiles.'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', args=[self.object.pk])
    
class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', args=[self.kwargs['pk']])
