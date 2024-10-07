# File: mini_fb/urls.py
# Author: Grace Wang (grace25@bu.edu), 10/7/2024
# Description: This file defines URL patterns for the mini Facebook application. 



from django.urls import path
from django.conf import settings
from . import views
from .views import *

# create a list of URLs for this app:
urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"), 

]