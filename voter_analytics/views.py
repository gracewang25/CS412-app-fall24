from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from .forms import VoterFilterForm
import plotly.express as px
import plotly.graph_objects as go

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    paginate_by = 100  # Set pagination to 100

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Use POST data for filtering if it's a POST request; otherwise, use GET for default loading
        if self.request.method == 'POST':
            form = VoterFilterForm(self.request.POST)
        else:
            form = VoterFilterForm(self.request.GET)  # This allows initial page load without filters

        # Apply filters if the form is valid
        if form.is_valid():
            queryset = form.filter_queryset(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pass form to the template
        form = VoterFilterForm(self.request.POST or self.request.GET)
        context['form'] = form

        return context
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Generate a Google Maps link based on the voter's address
        address = f"{self.object.street_number} {self.object.street_name}, {self.object.zip_code}"
        context['google_maps_link'] = f"https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')}"
        return context

from django.views.generic import TemplateView
from .models import Voter
import plotly.express as px
import plotly.graph_objects as go
from django.db import models

class GraphView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Define party affiliation mapping
        PARTY_MAP = {
            "U": "Unaffiliated",
            "D": "Democratic",
            "R": "Republican",
            "CC": "Constitution Party",
            "L": "Libertarian Party",
            "T": "Tea Party",
            "O": "Other",
            "G": "Green Party",
            "J": "Independent Party",
            "Q": "Reform Party",
            "FF": "Freedom Party"
        }

        # Distribution by Year of Birth
        birth_years = [voter.date_of_birth.year for voter in Voter.objects.all() if voter.date_of_birth]
        birth_year_histogram = px.histogram(
            x=birth_years, 
            title="Distribution of Voters by Year of Birth",
            color_discrete_sequence=["#4a7c59"]  # Dark green color for histogram bars
        )
        birth_year_histogram.update_layout(
            xaxis_title="Year of Birth",
            yaxis_title="Number of Voters"
        )
        context['birth_year_histogram'] = birth_year_histogram.to_html()

        # Distribution by Party Affiliation
        party_data = Voter.objects.exclude(party_affiliation__isnull=True).exclude(party_affiliation__exact="").values_list('party_affiliation', flat=True)
        cleaned_parties = [party.strip() for party in party_data if party.strip()]

        # Translate party codes to names using PARTY_MAP
        translated_parties = [PARTY_MAP.get(party, "Other") for party in cleaned_parties]

        # Aggregate counts for each party name
        party_counts = {party: translated_parties.count(party) for party in set(translated_parties)}
        parties = list(party_counts.keys())
        counts = list(party_counts.values())

        # Create the pie chart
        party_pie_chart = px.pie(
            names=parties,
            values=counts,
            title="Distribution of Voters by Party Affiliation",
            width=600,
            height=600,
            color_discrete_sequence=["#9caf88", "#4a7c59", "#6b8e23", "#8fbc8f", "#b0c4b1"]  # Shades of green for pie chart slices
        )
        context['party_pie_chart'] = party_pie_chart.to_html()

        # Distribution by Election Participation
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [Voter.objects.filter(**{election: True}).count() for election in elections]

        if all(count == 0 for count in election_counts):
            context['election_histogram'] = "<p>No data available for election participation.</p>"
        else:
            election_histogram = go.Figure(data=[go.Bar(x=elections, y=election_counts, marker_color="#4a7c59")])
            election_histogram.update_layout(
                title="Distribution of Voters by Election Participation",
                xaxis_title="Election",
                yaxis_title="Number of Voters",
                bargap=0.2
            )
            context['election_histogram'] = election_histogram.to_html()

        return context