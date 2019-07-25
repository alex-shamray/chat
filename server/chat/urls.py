from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.ChannelListView.as_view(), name='channel-list'),
    path('create/', views.ChannelCreateView.as_view(), name='channel-create'),
    path('<int:pk>/', views.ChannelDetailView.as_view(), name='channel-detail'),
]
