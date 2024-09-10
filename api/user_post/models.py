from django.db import models

# Create your models here.

from account.models import User
from common.models import BaseModelWithUID


class UserPost(BaseModelWithUID):
    user = models.ForeignKey(User, related_name="user_posts", on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    loves = models.ManyToManyField(User, related_name="loved_posts", blank=True)
    share = models.ManyToManyField(User, related_name="shared_posts", blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def number_of_loves(self):
        return self.loves.count()

    def number_of_share(self):
        return self.share.count()

    def __str__(self):
        return f"Post by {self.user.fname} at {self.created_at}"

    # def __str__(self):
    #     return(
    #         f"{self.user} "
    #         f"({self.created_at:%Y-%m-%d %H:%M}): "
    #         f"{self.body}..."
    #     )


class PostFile(BaseModelWithUID):
    post = models.ForeignKey(UserPost, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to="posts/files/")

    def __str__(self):
        return f"File for post {self.post.id} uploaded at {self.created_at}"


class Comment(BaseModelWithUID):
    post = models.ForeignKey(
        UserPost, related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="user_comments", on_delete=models.CASCADE
    )
    body = models.TextField()

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
