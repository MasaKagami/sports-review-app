from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from .models import Like
from reviews.models import Review
from .serializers import LikeSerializer

class LikeView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-like')
    def add_like(self, request, pk=None):
        review = get_object_or_404(Review, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, review=review)
        if created:
            return Response({'status': 'like added'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'like already exists'}, status=status.HTTP_409_CONFLICT)

    @action(detail=True, methods=['delete'], url_path='remove-like')
    def remove_like(self, request, pk=None):
        like = get_object_or_404(Like, user=request.user, review__pk=pk)
        like.delete()
        return Response({'status': 'like removed'}, status=status.HTTP_204_NO_CONTENT)
