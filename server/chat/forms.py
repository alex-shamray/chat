from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Channel


class ChannelCreationForm(forms.ModelForm):
    """
    A form that creates a messaging channel with members.
    """
    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea,
    )

    class Meta:
        model = Channel
        fields = ('members',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChannelCreationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return Channel.objects.create_channel(self.user, **self.cleaned_data)
