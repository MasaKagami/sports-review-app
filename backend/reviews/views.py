from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer

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
        serializer.save(user=self.request.user)  # Automatically sets the review's user to the current user

    def perform_update(self, serializer):
        review = get_object_or_404(Review, pk=serializer.instance.pk)
        if self.request.user == review.user:
            serializer.save()
        else:
            raise PermissionDenied("Cannot update another user's review!")

    def perform_destroy(self, instance):
        review = get_object_or_404(Review, pk=instance.pk)
        if self.request.user == review.user:
            instance.delete()
        else:
            raise PermissionDenied("Cannot delete another user's review!")

class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, tournament, slug):
        review = get_object_or_404(Review, user__username=username, game__slug=slug)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
