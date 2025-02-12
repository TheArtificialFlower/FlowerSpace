from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

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



class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_likes")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="p_likes")

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"


class BookMarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="u_bookmark")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="p_bookmark")

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.id}"



class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="unknown")
    desc = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now=True)



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
