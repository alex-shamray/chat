from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'channels', views.ChannelViewSet, basename='channel')
urlpatterns = router.urls
