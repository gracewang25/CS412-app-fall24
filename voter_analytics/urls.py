from django.urls import path
from . import views 
from .views import *


urlpatterns = [ 
    # map the URL (empty string) to the view

    path('', views.VoterListView.as_view(), name='voters'),
    path(r'voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
    path(r'graphs/', views.GraphView.as_view(), name='graphs'),
    
]