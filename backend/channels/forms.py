from django import forms
from .models import Channel


class ChannelForm(forms.ModelForm):
    channel_id = forms.CharField(max_length=100, label='YouTube Channel ID')