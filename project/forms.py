from django import forms
from django.contrib.auth.models import User
from .models import Org


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