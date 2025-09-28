from .models import Posts, Comment
from onlineshop.models import Coupons
from django.db.models.signals import post_save, post_delete
from utils.redis_manager import LikesRepository, BookmarkRepository, NotificationRepository, Notification
from django.dispatch import receiver
from accounts.models import Relations
from django.contrib.auth.models import User
from django.utils.timezone import now
from utils.utils import PostsCacheManager


@receiver(post_save, sender=Posts)
def update_posts_cache_on_save(sender, instance, **kwargs):
    """Update cache whenever a post is created or updated."""
    PostsCacheManager.update_posts()


@receiver(post_delete, sender=Posts)
def update_posts_cache_on_delete(sender, instance, **kwargs):
    """Update cache whenever a post is deleted."""
    PostsCacheManager.update_posts()


@receiver(post_delete, sender=Posts)
def cleanup_post_from_redis(sender, instance, **kwargs):
    post_id = instance.id
    likes_repo = LikesRepository()
    bookmarks_repo = BookmarkRepository()

    # cleanup likes
    users_liked = likes_repo.get_likes_for_post(post_id)
    for user_id in users_liked:
        likes_repo.redis.srem(f"user:{user_id}:likes", post_id)
    likes_repo.redis.delete(f"post:{post_id}:liked_by")

    # cleanup bookmarks
    users_bookmarked = bookmarks_repo.get_bookmarks_for_post(post_id)
    for user_id in users_bookmarked:
        bookmarks_repo.redis.srem(f"user:{user_id}:bookmarks", post_id)
    bookmarks_repo.redis.delete(f"post:{post_id}:bookmarked_by")




### ------------- NOTIFICATION SIGNALS ------------- ###
redis_class = NotificationRepository()

def create_like_notification(user_id, post_owner_id, post_id, liker_username):
    """Call manually in views when a post is liked."""
    if post_owner_id != user_id:
        notif = Notification(
            from_user=liker_username,
            message=f"{liker_username} liked your post.",
            created=now(),
            target_type="like",
            target_id=post_id
        ) # adjust for other funcs
        redis_class.add_notification(post_owner_id, notif)


@receiver(post_save, sender=Coupons)
def create_coupon_notifications(sender, instance, created, **kwargs):
    """Automatically notify all users about a new coupon."""
    if created:
        for user in User.objects.all():
            notif = Notification(
                from_user="system",
                message=f"New coupon!!! Use {instance.code} for {instance.discount}% discount!!",
                created=now(),
                target_type="coupon",
                target_id=user.id
            )
            redis_class.add_notification(user.id, notif)


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Notify post owner when someone comments."""
    if created:
        post_owner_id = instance.post.user.id
        commenter_id = instance.user.id
        if post_owner_id != commenter_id:
            notif = Notification(
                from_user=instance.user.username,
                message=f"{instance.user.username} commented on your post.",
                created=now(),
                target_type="comment",
                target_id=post_owner_id
            )
            redis_class.add_notification(post_owner_id, notif)


@receiver(post_save, sender=Relations)
def notify_new_follower(sender, instance, created, **kwargs):
    """Notify user when a new follower appears."""
    if created:
        followed_user_id = instance.to_user.id
        follower_username = instance.from_user.username
        notif = Notification(
            from_user=follower_username,
            message=f"{follower_username} started following you.",
            created=now(),
            target_type="follow",
            target_id=followed_user_id
        )
        redis_class.add_notification(followed_user_id, notif)


@receiver(post_save, sender=Posts)
def create_post_notification_for_followers(sender, instance, created, **kwargs):
    """Notify all followers when a user posts something new."""
    if created:
        followers_ids = Relations.objects.filter(to_user=instance.user).values_list('from_user', flat=True)
        for follower_id in followers_ids:
            notif = Notification(
                from_user=instance.user.username,
                message=f"{instance.user.username} has posted a new post.",
                created=now(),
                target_type="new_post",
                target_id=follower_id
            )
            redis_class.add_notification(follower_id, notif)