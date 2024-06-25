from rest_framework import serializers
from .models import Game
from reviews.serializers import ReviewSerializer

class GameDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = ['id', 'title', 'date', 'team1', 'team2', 'score_team1', 'score_team2','tournament', 'slug', 'reviews']
