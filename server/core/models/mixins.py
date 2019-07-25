from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AuthorMixin(models.Model):
    user_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='author_set')
    user_id = models.PositiveIntegerField()
    author = GenericForeignKey('user_type', 'user_id')

    class Meta:
        abstract = True


class GenericUserMixin(models.Model):
    user_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    user_id = models.PositiveIntegerField()
    user = GenericForeignKey('user_type', 'user_id')

    class Meta:
        abstract = True
