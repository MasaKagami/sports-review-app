from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.ReadOnlyField()  # To display the number of likes

    class Meta:
        model = Review
        fields = ['id', 'user', 'text', 'rating', 'created_at', 'likes_count']