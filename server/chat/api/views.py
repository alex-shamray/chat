from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .pagination import CursorPagination
from .serializers import ChannelSerializer, MessageSerializer
from ..models import Channel


class ChannelViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    pagination_class = CursorPagination

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        """
        return Channel.objects.get_all_channels_for_user(self.request.user)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        if self.action == 'messages':
            return MessageSerializer
        return ChannelSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(ChannelViewSet, self).get_serializer_context()
        if self.action == 'messages':
            context['channel'] = self.get_object()
        return context

    @action(detail=True, methods=['get', 'post'])
    def messages(self, request, *args, **kwargs):
        method = request.method.lower()
        if method == 'post':
            return self.create(request, *args, **kwargs)
        else:
            queryset = self.get_object().messages.order_by('-date_created')
            queryset = self.filter_queryset(queryset)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
