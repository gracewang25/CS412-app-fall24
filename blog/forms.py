#  blog/forms.py

from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''a form to create comment data'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Comment
        # fields = ['article', 'author', 'text', ]  # which fields from model should we use
        fields =  ['author', 'text']
