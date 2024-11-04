# File: mini_fb/views.py
# Author: Grace Wang (grace25@bu.edu), 10/7/2024
# Description: This file contains the Django class-based views for 
# the mini Facebook application. It includes the ShowAllProfilesView, 
# which displays all profiles.

from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from .models import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django import forms
from .models import Profile
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import *
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
# used to show that crud operations are read only using loginreq mixins
from django.contrib import messages





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

    # def get_object(self):
    #     # Retrieve the profile associated with the logged-in user
    #     return Profile.objects.get(user=self.request.user)

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', args=[self.object.pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    success_url = reverse_lazy('show_profile')

    # Users only can only update their profiles
    def get_object(self):
        # Get the profile for the logged-in user
        return Profile.objects.get(user=self.request.user)
    
    def get_success_url(self):
        # Redirect back to the profile page
        return reverse_lazy('show_profile', kwargs={'pk': self.object.pk})


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/create_status_form.html'

    # Override form_valid to manually set the profile
    def form_valid(self, form):
        # Use the logged-in user's profile directly
        profile = self.request.user.profile
        form.instance.profile = profile  # Set the profile for the status message
        
        # Save the status message
        sm = form.save()

        # Handle image uploads
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(status_message=sm, image_file=f)
        
        return super().form_valid(form)

    # Redirect back to the profile page after form submission
    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.request.user.profile.pk})



class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    
    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'
    success_url = reverse_lazy('show_profile')

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        profile_id = self.object.profile.pk
        # Redirect back to the profile page
        return reverse_lazy('show_profile', kwargs={'pk': profile_id})
    
class CreateFriendView(LoginRequiredMixin, View):
    '''A view to handle adding a friend relationship between profiles.'''

    def dispatch(self, request, *args, **kwargs):
        # Get the profile of the friend to be added
        other_profile_id = self.kwargs['other_pk']
        
        profile = request.user.profile
        other_profile = Profile.objects.get(pk=other_profile_id)

        # Prevent "self-friending"
        if profile.pk == other_profile.pk:
            messages.error(request, "You cannot add yourself as a friend.")
            return redirect(reverse_lazy('show_profile', kwargs={'pk': profile.pk}))

        # Check if the friend relationship already exists
        friend_exists = Friend.objects.filter(
            (Q(profile1=profile) & Q(profile2=other_profile)) |
            (Q(profile1=other_profile) & Q(profile2=profile))
        ).exists()

        # Only add the friend if the relationship does not exist
        if not friend_exists:
            Friend.objects.create(profile1=profile, profile2=other_profile)
            messages.success(request, f"You have successfully added {other_profile.user.username} as a friend.")


        # Redirect back to the current user's profile page
        return redirect(reverse_lazy('show_profile', kwargs={'pk': profile.pk}))
    
class ShowFriendSuggestionsView(DetailView):
    """A view to show friend suggestions for a profile."""
    
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        # Get the profile for the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggested_friends'] = self.object.get_friend_suggestions()
        return context
    
class ShowNewsFeedView(DetailView):
    """View to show the news feed for a specific profile."""
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        # Get the profile for the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the news feed for the profile
        context['news_feed'] = self.object.get_news_feed()
        return context
