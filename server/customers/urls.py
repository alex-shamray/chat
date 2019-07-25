from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup/$', views.CustomerSignupView.as_view(), name='customer-signup'),
]
