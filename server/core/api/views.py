from rest_framework import mixins
from rest_framework.generics import get_object_or_404, GenericAPIView


class SingletonGenericAPIView(GenericAPIView):
    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        obj = get_object_or_404(self.get_queryset())

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


# Concrete view classes that provide method handlers
# by composing the mixin classes with the base view.

class RetrieveSingletonAPIView(mixins.RetrieveModelMixin,
                               SingletonGenericAPIView):
    """
    Concrete view for retrieving a singleton model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RetrieveUpdateSingletonAPIView(mixins.RetrieveModelMixin,
                                     mixins.UpdateModelMixin,
                                     SingletonGenericAPIView):
    """
    Concrete view for retrieving, updating a singleton model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveCreateUpdateSingletonAPIView(mixins.RetrieveModelMixin,
                                           mixins.CreateModelMixin,
                                           mixins.UpdateModelMixin,
                                           SingletonGenericAPIView):
    """
    Concrete view for retrieving, creating, updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
