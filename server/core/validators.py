from django.contrib.auth import get_backends
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class UniqueUsernameValidator:
    message = _('This field must be unique.')
    code = 'invalid'
    instance = None

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer_field.parent, 'instance', None)

    def __call__(self, value):
        for backend in get_backends():
            if hasattr(backend, 'get_by_natural_key'):
                try:
                    user = backend.get_by_natural_key(value)
                    if user != self.instance:
                        raise ValidationError(self.message, code=self.code)
                except ObjectDoesNotExist:
                    pass
