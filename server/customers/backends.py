from django.contrib.auth.backends import ModelBackend

from .models import Customer


class CustomerBackend(ModelBackend):
    """
    Authenticates against Customer.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(Customer.USERNAME_FIELD)
        try:
            user = Customer.objects.get_by_natural_key(username)
        except Customer.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            Customer().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
