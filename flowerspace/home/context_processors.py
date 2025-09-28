from utils.redis_manager import LikesRepository, BookmarkRepository, NotificationRepository


def liked_and_bookmarked_posts(request):
    like_class = LikesRepository()
    bookmark_class = BookmarkRepository()
    liked_posts = []
    bookmarked_posts = []
    if request.user.is_authenticated:
        liked_posts = like_class.get_likes_for_user(request.user.id)
        bookmarked_posts = bookmark_class.get_bookmarks_for_user(request.user.id)
    return {'liked_posts': liked_posts, 'bookmarked_posts': bookmarked_posts}


def notifications(request):
    notif_class = NotificationRepository()
    notifs = notif_class.get_notifications(user_id=request.user.id)
    post_actions = ["like", "comment", "new_post"]
    return {'notifs':notifs, 'post_actions':post_actions}
