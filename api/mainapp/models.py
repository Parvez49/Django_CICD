from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from account.models import User


# User profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(
        default="thumbnail_logo.png", null=True, blank=True, upload_to="images/"
    )

    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    facebook_link = models.CharField(null=True, blank=True, max_length=100)
    linked_link = models.CharField(null=True, blank=True, max_length=100)
    instagram_link = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username


# Create profile when new user sign up
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

        # User have to follow themselve
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


# Post model
class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)
    loves = models.ManyToManyField(User, related_name="post_love", blank=True)
    post_image = models.ImageField(null=True, blank=True, upload_to="images/")

    # Keep track and count of likes
    def number_of_likes(self):
        return self.likes.count()

    # Keep track and count of love
    def number_of_loves(self):
        return self.loves.count()

    def __str__(self):
        return f"{self.user} " f"({self.created_at:%Y-%m-%d %H:%M}): " f"{self.body}..."


# Comments model
class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name="comments", on_delete=models.SET_NULL, null=True
    )
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.CharField(
        max_length=100,
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )
    comment_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        try:
            return f"{self.user.username} : {self.body[:30]}"
        except:
            return f"Anonymous : {self.body[:30]}"

    class Meta:
        ordering = ["-created_at"]


class UserPreference(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_preferences"
    )
    preference = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"{self.user}" f"{self.preference}"
