from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('newpost/', views.newpost, name="newpost"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('loginintro/', views.loginintro, name='loginintro'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('post_like/<int:pk>', views.post_like, name='post_like'),
    path('post_love/<int:pk>', views.post_love, name='post_love'),
    path('post_share/<int:pk>', views.post_share, name='post_share'),
    path('post_comments/<int:pk>', views.post_comments, name='post_comments'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('edit_post/<int:pk>', views.edit_post, name='edit_post'),
    path('search_post/', views.search_post, name='search_post'),
    path('search_user/', views.search_user, name='search_user'),
    path('comment_sent/<int:pk>', views.comment_sent, name='comment_sent'),
    path('update_preferance/', views.update_preferance, name='update_preferance'),
]
