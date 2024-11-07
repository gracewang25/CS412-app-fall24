from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from .forms import VoterFilterForm
import plotly.express as px
import plotly.graph_objects as go

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_list.html'
    paginate_by = 10
    ordering = ['last_name', 'first_name']  # Adjust ordering as necessary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = VoterFilterForm(self.request.GET or None)
        context['form'] = form

        # Apply filters if the form is valid
        if form.is_valid() and any(form.cleaned_data.values()):
            context['object_list'] = form.filter_queryset(self.get_queryset())
        else:
            context['object_list'] = self.get_queryset()

        return context
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Generate a Google Maps link based on the voter's address
        address = f"{self.object.street_number} {self.object.street_name}, {self.object.zip_code}"
        context['google_maps_link'] = f"https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')}"
        return context

class GraphView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Distribution by Year of Birth
        birth_years = [voter.date_of_birth.year for voter in Voter.objects.all() if voter.date_of_birth]
        birth_year_histogram = px.histogram(
            x=birth_years, 
            nbins=20, 
            title="Distribution of Voters by Year of Birth"
        )
        context['birth_year_histogram'] = birth_year_histogram.to_html()

        # Distribution by Party Affiliation
        party_counts = Voter.objects.values('party_affiliation').annotate(count=models.Count('party_affiliation'))
        parties = [party['party_affiliation'] for party in party_counts]
        counts = [party['count'] for party in party_counts]
        party_pie_chart = px.pie(
            names=parties, 
            values=counts, 
            title="Distribution of Voters by Party Affiliation", 
            width=600,  # Increased width
            height=600  # Increased height
        )
        context['party_pie_chart'] = party_pie_chart.to_html()

        # Distribution by Election Participation
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [Voter.objects.filter(**{election: True}).count() for election in elections]
        election_histogram = go.Figure(data=[go.Bar(x=elections, y=election_counts)])
        election_histogram.update_layout(title="Distribution of Voters by Election Participation")
        context['election_histogram'] = election_histogram.to_html()

        return context
