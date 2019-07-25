from django.contrib.auth.forms import UserCreationForm

from .models import Customer


class CustomerSignupForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user
