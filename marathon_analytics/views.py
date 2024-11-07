from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import *

# Create your views here.
class ResultsListView(ListView):
    '''view to display a list of marathon results'''
    # the bare minimum for a listview 
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = "results"

    paginate_by = 50

    def get_queryset(self) -> QuerySet[Any]:
        '''return the set of results'''

        # # use the superlcass ver of the queryset
        qs = super().get_queryset()
        # # return qs[:25]

        # filter qs by search parameter    
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            if city: # if not blank then filter by city
                qs  = Result.objects.filter(city=city)


        return qs