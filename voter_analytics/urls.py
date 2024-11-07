from django.urls import path
from . import views 


urlpatterns = [ 
    # map the URL (empty string) to the view
    path(r'', views.VotersListView.as_view(), name='voters'),
    path(r'results', views.ResultsListView.as_view(), name='results_list'),
    
]