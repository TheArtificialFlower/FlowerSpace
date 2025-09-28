from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from utils.redis_manager import LikesRepository


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Posts(models.Model):
    image = models.ImageField(upload_to="posts/")
    desc = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    hashtags = models.ManyToManyField(Hashtag)
    allow_comments = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def count_likes(self):
        redis_class = LikesRepository()
        post_id = self.id
        return len(redis_class.get_likes_for_post(post_id=post_id))




class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} commented for this post id: {self.post.id}"



class Article(models.Model):
    image = models.ImageField(upload_to="articles/")
    title = models.TextField(max_length=100)
    author = models.TextField(max_length=20)
    desc = CKEditor5Field()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
