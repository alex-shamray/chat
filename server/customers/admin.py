from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name')
    list_filter = ('is_active',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()
