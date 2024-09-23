## hw/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app:
urlpatterns = [
    path(r'', views.home, name="home"), 
    path(r'quote', views.quote, name="quote"), 
    path(r'about', views.about, name="about"),
    path('show_all', views.show_all, name='show_all'),


]