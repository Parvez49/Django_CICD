from django.shortcuts import render, get_object_or_404

# Create your views here.

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import UserPost, PostFile, Comment
from .serializers import (
    UserPostSerializer,
    PostFileSerializer,
    PostDetailSerializer,
    CommentSerializer,
)


class AddCommentPostAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = get_object_or_404(UserPost, id=post_id)
        serializer.save(user=self.request.user, post=post)


class LovePostView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        post = get_object_or_404(UserPost, id=post_id)
        user = request.user

        if post.loves.filter(id=user.id).exists():
            post.loves.remove(user)
            message = "You have removed your love from this post."
        else:
            post.loves.add(user)
            message = "You have loved this post."

        return Response(
            {
                "status": "success",
                "message": message,
                "loves_count": post.number_of_loves(),
            },
            status=status.HTTP_200_OK,
        )


class LikePostView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        post = get_object_or_404(UserPost, id=post_id)
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            message = "You unliked this post."
        else:
            post.likes.add(user)
            message = "You liked this post."

        return Response(
            {
                "status": "success",
                "message": message,
                "likes_count": post.number_of_likes(),
            },
            status=status.HTTP_200_OK,
        )


class UserPostListCreateAPIView(generics.ListCreateAPIView):
    # queryset = UserPost.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    filterset_fields = ["user"]

    def get_queryset(self):
        user = self.request.user
        return UserPost.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPost.objects.all()
    # serializer_class = UserPostSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostDetailSerializer
        else:
            return UserPostSerializer
