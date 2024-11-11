# voter_analytics/forms.py

from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    PARTY_CHOICES = [
        ('', 'All'),
        ('D', 'Democratic'),
        ('R', 'Republican'),
        ('U', 'Unaffiliated'),
        ('L', 'Libertarian Party'),
        ('T', 'Tea Party'),
        ('O', 'Other'),
        ('G', 'Green Party'),
        ('J', 'Independent Party'),
        ('Q', 'Reform Party'),
        ('FF', 'Freedom Party'),
    ]
    
    VOTER_SCORE_CHOICES = [
        ('', 'All'),
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]

    party_affiliation = forms.ChoiceField(choices=PARTY_CHOICES, required=False, label="Party Affiliation")
    min_birth_year = forms.IntegerField(required=False, label="Born After (Year)")
    max_birth_year = forms.IntegerField(required=False, label="Born Before (Year)")
    voter_score = forms.ChoiceField(choices=VOTER_SCORE_CHOICES, required=False, label="Voter Score")
    v20state = forms.BooleanField(required=False, label="Voted in 2020 State Election")
    v21town = forms.BooleanField(required=False, label="Voted in 2021 Town Election")
    v21primary = forms.BooleanField(required=False, label="Voted in 2021 Primary Election")
    v22general = forms.BooleanField(required=False, label="Voted in 2022 General Election")
    v23town = forms.BooleanField(required=False, label="Voted in 2023 Town Election")

    def filter_queryset(self, queryset):
        if self.cleaned_data['party_affiliation']:
            queryset = queryset.filter(party_affiliation=self.cleaned_data['party_affiliation'])
        if self.cleaned_data['min_birth_year']:
            queryset = queryset.filter(date_of_birth__year__gte=self.cleaned_data['min_birth_year'])
        if self.cleaned_data['max_birth_year']:
            queryset = queryset.filter(date_of_birth__year__lte=self.cleaned_data['max_birth_year'])
        if self.cleaned_data['voter_score']:
            queryset = queryset.filter(voter_score=self.cleaned_data['voter_score'])
        if self.cleaned_data['v20state']:
            queryset = queryset.filter(v20state=True)
        if self.cleaned_data['v21town']:
            queryset = queryset.filter(v21town=True)
        if self.cleaned_data['v21primary']:
            queryset = queryset.filter(v21primary=True)
        if self.cleaned_data['v22general']:
            queryset = queryset.filter(v22general=True)
        if self.cleaned_data['v23town']:
            queryset = queryset.filter(v23town=True)
        return queryset
