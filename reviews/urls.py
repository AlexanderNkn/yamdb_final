from django.urls import path, include
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register("", ReviewViewSet, basename="reviews")
router.register("(?P<review_id>\d+)/comments", CommentViewSet, basename="comments")


urlpatterns = [path("", include(router.urls))]
