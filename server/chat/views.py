from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import ChannelCreationForm
from .models import Person, Channel


class ChatMixin(ContextMixin):
    """
    A mixin that provides a way to show the number of unread channels
    for the current user in a request.
    """

    def get_context_data(self, **kwargs):
        """
        Insert the number of unread channels for the current user into
        the context dict.
        """
        if 'unread_channels' not in kwargs:
            kwargs['unread_channels'] = Channel.objects.get_unread_channels_for_user(self.request.user).count()
        if self.request.user.is_authenticated:
            kwargs['person'] = Person.objects.get_for_user(self.request.user)
        return super().get_context_data(**kwargs)


class ChannelListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        return Channel.objects.get_all_channels_for_user(self.request.user)


class ChannelDetailView(LoginRequiredMixin, ChatMixin, DetailView):
    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        """
        return Channel.objects.get_all_channels_for_user(self.request.user)


class ChannelCreateView(LoginRequiredMixin, CreateView):
    model = Channel
    form_class = ChannelCreationForm

    def get_form_kwargs(self):
        """
        Return the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
