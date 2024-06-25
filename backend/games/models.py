from django.db import models
from django.utils.text import slugify

class Game(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    score_team1 = models.IntegerField(default=0)  # Default score for team1
    score_team2 = models.IntegerField(default=0)  # Default score for team2
    tournament = models.CharField(max_length=100)  # Mandatory tournament field
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.tournament}-{self.team1}-{self.team2}")
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.tournament})"