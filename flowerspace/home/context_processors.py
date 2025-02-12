from .models import Likes, BookMarks, Notifications

def liked_and_bookmarked_posts(request):
    if request.user.is_authenticated:
        liked_posts = Likes.objects.filter(user=request.user).values_list('post_id', flat=True)
        bookmarked_posts = BookMarks.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        liked_posts = []
        bookmarked_posts = []

    return {
        'liked_posts': liked_posts,
        'bookmarked_posts': bookmarked_posts,
    }


def notifications(request):
    if request.user.is_authenticated:
        notifs = Notifications.objects.filter(user=request.user).order_by("-created")
    else:
        notifs = []

    return {
        'notifs':notifs
    }
