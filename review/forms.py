from django import forms
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image']


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description']