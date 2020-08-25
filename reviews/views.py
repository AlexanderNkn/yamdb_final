from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets, permissions, pagination, serializers

from contents.models import Title
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsOwnerAdminModeratorToEdit


class NestedResourceMixin:
    """
    Mixin for GenericAPIView for nested resources. E.g., in /movies/<movie_id>/reviews/ 
    the 'Review.movie' field references 'Movie' objects identified by <movie_id>.
    Requires class attributes parent_object, parent_field, parent_url_id and
    the _serializer_save_fields method.
    """

    _parent_object, _parent_field, _parent_url_id = None, None, None

    def _serializer_save_fields(self):
        return {}

    def _get_parent(self):
        return get_object_or_404(
            self._parent_object, id=self.kwargs[self._parent_url_id]
        )

    def get_queryset(self):
        parent = self._get_parent()
        return super().get_queryset().filter(**{self._parent_field: parent})

    def perform_create(self, serializer):
        parent = self._get_parent()
        serializer.save(
            **{self._parent_field: parent}, **self._serializer_save_fields()
        )


class ReviewViewSet(NestedResourceMixin, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerAdminModeratorToEdit,
    ]
    _parent_object, _parent_field, _parent_url_id = Title, "title", "title_id"

    def perform_create(self, serializer):
        self._pre_perform_create()
        super().perform_create(serializer)

    def _serializer_save_fields(self):
        return {"author": self.request.user}

    def _pre_perform_create(self):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        if Review.objects.filter(author=self.request.user, title=title).exists():
            raise serializers.ValidationError(
                "You can only leave one review per title."
            )


class CommentViewSet(NestedResourceMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerAdminModeratorToEdit,
    ]
    _parent_object, _parent_field, _parent_url_id = Review, "review", "review_id"

    def _serializer_save_fields(self):
        return {"author": self.request.user}
