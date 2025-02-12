from .models import Posts, Notifications, Comment, Likes
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Relations
from django.contrib.auth.models import User


def check_notif_limit(user):
    if Notifications.objects.filter(user=user).count() >= 10:
        Notifications.objects.filter(user=user).order_by('created').first().delete()



@receiver(post_save, sender=Likes)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        content = f"{instance.user.username} liked your post."
        check_notif_limit(post.user)
        if post.user != instance.user:
            Notifications.objects.create(
                user=post.user,
                from_user=instance.user,
                desc=content
            )



@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        content = f"{instance.user.username} commented on your post."
        check_notif_limit(post.user)
        if post.user != instance.user:
            Notifications.objects.create(
                user=post.user,
                from_user=instance.user,
                desc=content
            )



@receiver(post_save, sender=Relations)
def notify_new_follower(sender, instance, created, **kwargs):
    if created:
        followed_user = instance.to_user
        follower = instance.from_user
        content = f"{follower.username} started following you."
        Notifications.objects.create(
            user=followed_user,
            from_user=follower,
            desc=content
        )



@receiver(post_save, sender=Posts)
def create_post_notification_for_followers(sender, instance, created, **kwargs):
    if created:

        followers_ids = Relations.objects.filter(to_user=instance.user).values_list('from_user', flat=True)
        followers = User.objects.filter(id__in=followers_ids)
        for follower in followers:
            check_notif_limit(follower)
            content = f"{instance.user.username} has posted a new post."
            Notifications.objects.create(
                user=follower,
                from_user=instance.user,
                desc=content
            )