from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserRelationship, User, Profile, UserActivity, STATUS_CHOICES


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserActivity.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=UserRelationship)
def post_save_add_to_friends(sender, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    status_ = instance.status
    if status_ == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()
