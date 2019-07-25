from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^storage/(?P<path>[-\w_/.]+)$', views.FileDownloadView.as_view(), name='file-download'),
]
