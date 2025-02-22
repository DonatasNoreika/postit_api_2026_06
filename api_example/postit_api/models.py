from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=2000)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='pictures', null=True)

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    post = models.ForeignKey(to="Post", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.body} ({self.user.username} - {self.created})"


class PostLike(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to="Post", on_delete=models.CASCADE)


class CommentLike(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comment = models.ForeignKey(to="Comment", on_delete=models.CASCADE)
