from django.contrib import admin
from .models import Hashtag, Posts, Comment, Article

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'desc', 'allow_comments', 'created', 'updated')
    list_filter = ('allow_comments', 'created', 'updated')
    search_fields = ('desc',)
    ordering = ('-created',)
    filter_horizontal = ('hashtags',)  # Allows easy selection of hashtags



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "text", "created")
    list_filter = ("created", "user")
    search_fields = ("user__username", "post__title", "text")
    ordering = ("-created",)
    readonly_fields = ("created",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created", "updated")
    list_filter = ("created", "updated", "author")
    search_fields = ("title", "author")
    ordering = ("-created",)
    readonly_fields = ("created", "updated")



