from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.views import APIView
from .serializers import UserSerializer, ReviewSerializer, GameDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Game, Review, Like

from django.shortcuts import get_object_or_404

# Create your views here.

# to create user
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ReviewListCreateView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Review.objects.all()
        return Review.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Automatically sets the review's user to the current user

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.user:
            serializer.save()
        else:
            raise PermissionDenied("Cannot update another user's review!")

    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
        else:
            raise PermissionDenied("Cannot delete another user's review!")

class LikeView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-like')
    def add_like(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            like, created = Like.objects.get_or_create(user=request.user, review=review)
            if created:
                return Response({'status': 'like added'}, status=status.HTTP_201_CREATED)
            return Response({'status': 'like already exists'}, status=status.HTTP_409_CONFLICT)
        except Review.DoesNotExist:
            raise NotFound("Review not found")

    @action(detail=True, methods=['delete'], url_path='remove-like')
    def remove_like(self, request, pk=None):
        try:
            like = Like.objects.get(user=request.user, review__pk=pk)
            like.delete()
            return Response({'status': 'like removed'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            raise NotFound("Like not found")
        
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer
    permission_classes = [IsAuthenticated]

class GameDetailView(APIView):
    def get(self, request, tournament, slug):
        game = get_object_or_404(Game, slug=slug)
        serializer = GameDetailSerializer(game)
        return Response(serializer.data)

class ReviewDetailView(APIView):
    def get(self, request, username, tournament, slug):
        review = get_object_or_404(Review, user__username=username, game__slug=slug)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)