from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.http import StreamingHttpResponse
from django.utils.http import http_date
from django.utils.http import is_safe_url
from django.views.generic.base import View
from django.views.generic.edit import FormMixin


class SuccessURLMixin(SuccessURLAllowedHostsMixin, FormMixin):
    """Provide the URL to redirect to after processing a valid form."""

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        """
        url = self.get_redirect_url()
        return url or super().get_success_url()

    def get_redirect_url(self):
        """
        Return the user-originating redirect URL if it's safe.
        """
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''


class DownloadView(View):
    """
    https://djangosnippets.org/snippets/2549/
    Generic class view to abstract out the task of serving up files from within Django.
    Recommended usage is to combine it with SingleObjectMixin and extend certain methods based on your particular use case.

    Example usage::

        class Snippet(models.Model):
            name = models.CharField(max_length = 100)
            slug = SlugField()
            code = models.TextField()

        from django.views.generic.detail import SingleObjectMixin

        class DownloadSnippetView(SingleObjectMixin, DownloadView):
            model = Snippet
            content_type = 'application/python'

           def get_contents(self):
                return self.get_object().code

            def get_filename(self):
                return self.get_object().slug + '.py'
    """

    content_type = None
    extension = None
    filename = None

    def get_filename(self):
        return self.filename

    def get_extension(self):
        return self.extension

    def get_content_type(self):
        return self.content_type

    def get_last_modified(self):
        pass

    def get_content_length(self):
        pass

    def get_contents(self):
        """ Returns the contents of the file download. """
        pass

    def get(self, request, *args, **kwargs):
        response = StreamingHttpResponse(self.get_contents(), content_type=self.get_content_type())
        if self.get_filename():
            response['Content-Disposition'] = 'filename=' + self.get_filename()
        response['Last-Modified'] = http_date(self.get_last_modified())
        response['Content-Length'] = self.get_content_length()

        return response
