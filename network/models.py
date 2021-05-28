from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:

        # sorted in descending order, newer posts are returned first
        ordering = ["-created"]


    def serialize(self):
        return {
            'user': self.user.id,
            'content': self.content
        }

    def __str__(self):
        if self.created == self.modified:
            return f'{self.user} posted {self.content}, on {self.created}'
        else:
            return f'{self.user} posted {self.content}, modified on {self.modified}'

class Like(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.post} on {self.created}"


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:

        # ensures each follow-followed relation is unique
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

        ordering = ["-created"]
