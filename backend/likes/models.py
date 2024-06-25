from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from reviews.models import Review

# Create your models here.
class Like(models.Model):
    review = models.ForeignKey(Review, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')  # Ensures a user can like a review only once

@receiver(post_save, sender=Like)
def increment_like_count(sender, instance, created, **kwargs):
    if created:
        instance.review.likes_count += 1
        instance.review.save(update_fields=['likes_count'])

@receiver(post_delete, sender=Like)
def decrement_like_count(sender, instance, **kwargs):
    instance.review.likes_count -= 1
    instance.review.save(update_fields=['likes_count'])