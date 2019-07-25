from django.contrib import admin

from .models import Channel


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'messages_count')

    def get_readonly_fields(self, request, obj=None):
        """
        Hook for specifying custom readonly fields.
        """
        # make all fields readonly
        return [field.name for field in self.opts.fields]

    def has_add_permission(self, request):
        """
        Returns True if the given request has permission to add an object.
        """
        return False
