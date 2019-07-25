from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from profiles.models import ProfileMixin


class CustomerManager(BaseUserManager):
    def create_customer(self, email, password, **extra_fields):
        """
        Creates and saves a Customer with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        customer = self.model(email=email, **extra_fields)
        customer.set_password(password)
        customer.save(using=self._db)
        return customer


class Customer(AbstractBaseUser, ProfileMixin):
    """
    Customers within the Django authentication system are represented by this
    model.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A customer with that email already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomerManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')


class CustomerMixin(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, verbose_name=_('customer'))

    class Meta:
        abstract = True
