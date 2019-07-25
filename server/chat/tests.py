import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from chat.models import Person, Channel, Message

UserModel = get_user_model()


def create_user():
    """
    Create a user with the random `username`.
    """
    user = UserModel.objects.create_user(str(uuid.uuid4())[:10])
    user.person = Person.objects.get_for_user(user)
    return user


def create_channel(creator):
    """
    Create a chat channel with the given channel's creator and random
    members.
    """
    members = [create_user().person for i in range(2)]
    return Channel.objects.create_channel(creator, members, 'Initial message')


def create_message(channel, author):
    """
    Create a message within the given chat channel and the given
    message's author.
    """
    body = 'Message {}'.format(uuid.uuid4())
    return Message.objects.create(channel=channel, author=author, body=body)


class ChannelModelTests(TestCase):
    pass


class ChannelListViewTests(TestCase):
    def test_no_channels(self):
        """
        If no channels exist, an appropriate message is displayed.
        """
        self.client.force_login(create_user())

        response = self.client.get(reverse('chat:channel-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No messages yet.')
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_channel_with_membership(self):
        """
        Channels with a membership of the current user are displayed on the
        index page.
        """
        creator = create_user()
        create_channel(creator)

        self.client.force_login(creator)

        response = self.client.get(reverse('chat:channel-list'))
        self.assertQuerysetEqual(
            response.context['object_list'],
            ['<Channel: Channel object>']
        )

    def test_channel_without_membership(self):
        """
        Channels without a membership of the current user aren't displayed on
        the index page.
        """
        create_channel(create_user())

        self.client.force_login(create_user())

        response = self.client.get(reverse('chat:channel-list'))
        self.assertContains(response, 'No messages yet.')
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_two_channels(self):
        """
        The channels index page may display multiple channels.
        """
        creator = create_user()
        create_channel(creator)
        create_channel(creator)

        self.client.force_login(creator)

        response = self.client.get(reverse('chat:channel-list'))
        self.assertQuerysetEqual(
            response.context['object_list'],
            ['<Channel: Channel object>', '<Channel: Channel object>']
        )


class ChannelDetailViewTests(TestCase):
    def test_channel_without_membership(self):
        """
        The detail view of a channel without a membership of the current user
        returns a 404 not found.
        """
        channel = create_channel(create_user())

        self.client.force_login(create_user())

        url = reverse('chat:channel-detail', args=(channel.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_channel_with_membership(self):
        """
        The detail view of a channel with a membership of the current user
        displays the channel's text.
        """
        creator = create_user()
        channel = create_channel(creator)

        self.client.force_login(creator)

        url = reverse('chat:channel-detail', args=(channel.id,))
        response = self.client.get(url)
        self.assertContains(response, channel.id)
