from django import forms
from django.contrib.auth.models import User
from .models import *


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['rental_date', 'return_date']

    def clean(self):
        cleaned_data = super().clean()
        rental_date = cleaned_data.get("rental_date")
        return_date = cleaned_data.get("return_date")

        # Validate that return_date is after rental_date
        if rental_date and return_date and return_date <= rental_date:
            raise forms.ValidationError("Return date must be after the rental date.")

        return cleaned_data

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        """Override save to handle setting the user's password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class OrgRegistrationForm(forms.ModelForm):
    class Meta:
        model = Org
        fields = ['name', 'email', 'venmo_username', 'location', 'profile_picture', 'description']

from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            'name', 'description', 'item_type', 'prop', 'size_xs', 'size_s', 'size_m', 'size_l',
            'size_xl', 'pricing_per_unit', 'usage_type', 'image'
        ]

class OrgUpdateForm(forms.ModelForm):
    """Form for updating Org (organization) profile."""

    class Meta:
        model = Org
        fields = ['name', 'email', 'location', 'profile_picture', 'description', 'venmo_username']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'venmo_username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venmo Username'}),
        }