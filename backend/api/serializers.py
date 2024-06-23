from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Game
from .models import Review
from .models import Like

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            "password": {"write_only": True, "style": {'input_type': 'password'}}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.ReadOnlyField()  # To display the number of likes

    class Meta:
        model = Review
        fields = ['id', 'user', 'text', 'rating', 'created_at', 'likes_count']

class GameDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = ['id', 'title', 'date', 'tournament', 'team1', 'team2', 'slug', 'reviews']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'review', 'user']
