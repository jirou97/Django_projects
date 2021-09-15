from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

GENDERS = [
    ('M','Male'),
    ('F','Female'),
    ('O','Other')
]
class User(AbstractUser):
    timestamp = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    image = models.ImageField(default='static/image/user-male.png')
    gender = models.CharField(max_length=1, choices=GENDERS, default = 'O')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.CharField(max_length=400, default=None)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_edited = models.DateTimeField(default=timezone.now)

    def serialize(self):
        likes = Likes.objects.filter(post=self)
        like = len(likes)
        users = set()
        comments = Comment.objects.filter(post=self)
        comm = len(comments)
        for x in likes:
            users.add(x.user)
        return {
            "id": self.id,
            "user": self.user,
            "body": self.body,
            "timestamp_created": self.timestamp_created,
            "timestamp_edited": self.timestamp_edited,
            "likes": like,
            "likers": users,
            "comments":comm,
            "followers": [x.user for x in Follow.objects.filter(follower=self.user)]
        }


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="has_comments")
    comment = models.CharField(max_length=200, default="")
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_edited = models.DateTimeField(default=timezone.now)


class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="has_followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_edited = models.DateTimeField(default=timezone.now)


class Likes(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="has_likes")
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_edited = models.DateTimeField(default=timezone.now)