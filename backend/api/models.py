from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify


# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    tournament = models.CharField(max_length=100, blank=True, null=True)  # Optional: adjust based on your needs
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.tournament}-{self.team1}-{self.team2}")
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.tournament})"

class Review(models.Model):
    game = models.ForeignKey(Game, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)  # Caches the number of likes

    def __str__(self):
        return f"Review by {self.user.username} on {self.game.title}"
    
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