from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .management import create_persons


class ChatConfig(AppConfig):
    name = 'chat'

    def ready(self):
        post_migrate.connect(create_persons, sender=self)
