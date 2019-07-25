import magic
from django.core.files.storage import default_storage
from django.utils.functional import cached_property

from ..views import DownloadView


class FileDownloadView(DownloadView):
    @cached_property
    def file(self):
        storage = default_storage
        name = self.kwargs['path']
        return storage.open(name)

    def get_filename(self):
        # return self.kwargs['path'].split('/')[-1]
        pass

    def get_content_type(self):
        f = magic.Magic(mime=True)
        self.file.seek(0)
        return f.from_buffer(self.file.read())

    def get_last_modified(self):
        return default_storage.get_modified_time(self.kwargs['path']).timestamp()

    def get_content_length(self):
        return self.file.size

    def get_contents(self):
        self.file.seek(0)
        return self.file
