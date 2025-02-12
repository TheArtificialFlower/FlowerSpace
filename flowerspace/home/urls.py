from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("post/create/", views.CreatePostView.as_view(), name="post_create"),
    path("post/details/<int:post_id>/", views.PostDetailsView.as_view(), name="post_details"),
    path("post/like/<int:id>/", views.ToggleLikeView.as_view(), name="post_like"),
    path("post/delete/<int:pk>/", views.PostDeleteView.as_view(), name="post_delete"),
    path("post/bookmark/<int:id>/", views.ToggleBookmarkView.as_view(), name="post_bookmark"),
    path("articles/", views.ArticleView.as_view(), name="articles"),
    path("articles/<int:article_id>/", views.ArticleDetailsView.as_view(), name="article_details")
]