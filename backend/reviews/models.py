from django.db import models
from django.contrib.auth.models import User
from games.models import Game
# Create your models here.

class Review(models.Model):
    game = models.ForeignKey(Game, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)  # Caches the number of likes

    def __str__(self):
        return f"Review by {self.user.username} on {self.game.title}"