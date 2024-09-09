from django.urls import path

from . import views

urlpatterns = [
    path('/<int:post_id>/comments', views.AddCommentPostAPIView.as_view(), name='add-comment'),
    path('/<int:post_id>/love', views.LovePostView.as_view(), name='love-post'),
    path('/<int:post_id>/like', views.LikePostView.as_view(), name='like-post'),
    path('/<int:pk>', views.UserPostRetrieveUpdateDestroyAPIView.as_view(), name='userpost-retrieve-update-destroy'),
    path('', views.UserPostListCreateAPIView.as_view(), name='userpost-list-create'),
]
