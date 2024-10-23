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
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


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
    
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    success_url = reverse_lazy('show_profile')

    def get_success_url(self):
        # Redirect back to the profile page
        return reverse_lazy('show_profile', kwargs={'pk': self.object.pk})
    
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/create_status_form.html'
    
    # Override form_valid to manually set the profile
    def form_valid(self, form):
        profile_id = self.kwargs['pk']  # Get the profile ID from the URL
        profile = Profile.objects.get(pk=profile_id)  # Retrieve the Profile object
        
        # Set the profile field before saving
        form.instance.profile = profile
        
        # Save the status message
        sm = form.save()

        # Handle image uploads
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(status_message=sm, image_file=f)
        
        return super().form_valid(form)

    # Redirect back to the profile page after form submission
    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.kwargs['pk']})
    
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    
    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'
    success_url = reverse_lazy('show_profile')

    def get_success_url(self):
        profile_id = self.object.profile.pk
        # Redirect back to the profile page
        return reverse_lazy('show_profile', kwargs={'pk': profile_id})