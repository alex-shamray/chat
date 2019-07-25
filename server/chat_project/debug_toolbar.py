from django.conf import settings


def show_toolbar(request):
    """
    Function to determine whether to show the toolbar on a given page.
    """
    return bool(settings.DEBUG)
