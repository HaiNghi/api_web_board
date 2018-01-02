from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from web_board import views
from rest_framework.schemas import get_schema_view

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'board', views.BoardViewSet)
router.register(r'topic', views.TopicViewSet)
router.register(r'post', views.PostViewSet)

# schema_view = get_schema_view(title='Pastebin API')
# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^schema/$', schema_view),
]
