from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models import F
from django.utils.translation import ugettext_lazy as _

from core.models.mixins import GenericUserMixin


class PersonManager(models.Manager):
    def get_for_user(self, user):
        """
        Return the Person object for a given user, creating the
        Person if necessary.
        """
        person, created = self.get_or_create(
            user_type=ContentType.objects.get_for_model(user),
            user_id=user.pk,
        )
        return person


class Person(GenericUserMixin):
    objects = PersonManager()

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return str(self.user)


class ChannelManager(models.Manager):
    @transaction.atomic
    def create_channel(self, initiator, members, message):
        """
        Creates and saves a Channel with the given initiator, members and message.
        """
        if not initiator:
            raise ValueError('The given initiator must be set')
        channel = self.create()
        author = Person.objects.get(user_type=ContentType.objects.get_for_model(initiator), user_id=initiator.id)
        channel.membership_set.create(person=author)
        for user in members:
            channel.membership_set.create(person=user)
        channel.messages.create(author=author, body=message)
        return channel

    def get_all_channels_for_user(self, user):
        """
        Returns all channels for the user given.
        """
        return self.filter(
            members__user_type=ContentType.objects.get_for_model(user),
            members__user_id=user.id,
        ).distinct().prefetch_related('members').order_by('-date_created')

    def get_unread_channels_for_user(self, user):
        """
        Returns unread channels for the user given.
        """
        return self.filter(
            members__user_type=ContentType.objects.get_for_model(user),
            members__user_id=user.id,
            membership__last_read_message_index__lt=F('messages_count'),
        )


class Channel(models.Model):
    messages_count = models.PositiveIntegerField(_('number of messages'), default=0)
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('channel', 'person'),
    )
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    objects = ChannelManager()

    @property
    def last_message(self):
        """
        Returns the last received message.
        """
        return self.messages.latest('date_created')

    def mark_read(self, user):
        """
        Marks the channel as read for a particular user.
        """
        self.membership_set.filter(person=user).update(last_read_message_index=self.messages_count)

    def has_unread_messages(self, user):
        """
        Returns True if the channel has any unread messages for the given user.
        """
        return self.messages_count > self.member_set.get(user=user).last_read_message_index


class Membership(models.Model):
    channel = models.ForeignKey(Channel, models.CASCADE, verbose_name=_('channel'))
    person = models.ForeignKey(Person, models.CASCADE, verbose_name=_('person'))
    last_read_message_index = models.PositiveIntegerField(
        _('last read message index'),
        default=0,
        help_text=_('The index of the last message this member has read within this channel.'),
    )

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
        unique_together = (('channel', 'person'),)


class Message(models.Model):
    channel = models.ForeignKey(Channel, models.CASCADE, verbose_name=_('channel'), related_name='messages')
    author = models.ForeignKey(Person, models.CASCADE, verbose_name=_('author'))
    body = models.TextField(_('body'))
    index = models.PositiveIntegerField(
        _('index'),
        help_text=_('The index of the message within the channel.'),
    )
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)

    def save(self, *args, **kwargs):
        """
        Saves the current instance.
        """
        if self.pk is None:
            self.channel.messages_count += 1
            self.channel.save(update_fields=['messages_count'])

            self.channel.mark_read(self.author)

            self.index = self.channel.messages_count
        super().save(*args, **kwargs)
