import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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


class ChannelTests(APITestCase):
    def test_create_channel(self):
        """
        Ensure we can create a new chat channel.
        """
        creator = create_user()
        member1 = create_user().person
        member2 = create_user().person

        self.client.force_authenticate(user=creator)

        url = reverse('channel-list')
        data = {
            'members': [
                {'id': member1.id},
                {'id': member2.id},
            ],
            'message': 'Hi!',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        channel = Channel.objects.get(pk=response.data['id'])
        self.assertEqual(channel.members.count(), 3)
        self.assertEqual(channel.messages.count(), 1)
        self.assertEqual(channel.messages.get().body, 'Hi!')

    def test_create_channel_with_non_existent_user(self):
        """
        Ensure we can't create a new chat channel with a non-existent user.
        """
        creator = create_user()

        self.client.force_authenticate(user=creator)

        url = reverse('channel-list')
        data = {
            'members': [{'id': 0}],
            'message': 'Hi!',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_channel_without_users(self):
        """
        Ensure we can't create a new chat channel without users.
        """
        creator = create_user()

        self.client.force_authenticate(user=creator)

        url = reverse('channel-list')
        data = {
            'members': [],
            'message': 'Hi!',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_no_channels(self):
        """
        If no chat channels exist, an empty list is returned.
        """
        self.client.force_authenticate(user=create_user())

        url = reverse('channel-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_list_channels_with_membership(self):
        """
        Channels with a membership of the current user are returned.
        """
        creator = create_user()
        create_channel(creator)

        self.client.force_authenticate(user=creator)

        url = reverse('channel-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_channels_without_membership(self):
        """
        Channels without a membership of the current user aren't returned.
        """
        create_channel(create_user())

        self.client.force_authenticate(user=create_user())

        url = reverse('channel-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_list_two_channels(self):
        """
        Ensure we can retrieve multiple channels.
        """
        creator = create_user()
        create_channel(creator)
        create_channel(creator)

        self.client.force_authenticate(user=creator)

        url = reverse('channel-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_send_message(self):
        """
        Ensure we can send a message.
        """
        creator = create_user()
        channel = create_channel(creator)

        self.client.force_authenticate(user=creator)

        url = reverse('channel-messages', args=(channel.id,))
        data = {'body': 'Test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        channel.refresh_from_db()
        self.assertEqual(channel.last_message.body, 'Test')
        self.assertEqual(channel.messages_count, 2)
        self.assertEqual(channel.messages.count(), 2)

    def test_send_empty_message(self):
        """
        Ensure we can't send an empty message.
        """
        creator = create_user()
        channel = create_channel(creator)

        self.client.force_authenticate(user=creator)

        url = reverse('channel-messages', args=(channel.id,))
        data = {'body': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        channel.refresh_from_db()
        self.assertEqual(channel.messages_count, 1)
        self.assertEqual(channel.messages.count(), 1)

    def test_list_two_messages(self):
        """
        Ensure we can retrieve multiple messages.
        """
        creator = create_user()
        channel = create_channel(creator)
        create_message(channel, create_user().person)

        self.client.force_authenticate(user=creator)

        url = reverse('channel-messages', args=(channel.id,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
