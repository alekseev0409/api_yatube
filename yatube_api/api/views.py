from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework import viewsets, mixins

from .permissions import (
    AuthorPermission
)
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer
)
from posts.models import Post, Group, User


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        AuthorPermission
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorPermission, permissions.IsAuthenticated]

    def get_post(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(
    viewsets.ReadOnlyModelViewSet
):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
