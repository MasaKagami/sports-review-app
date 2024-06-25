from django.shortcuts import render
from .models import Game
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import GameDetailSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer
    permission_classes = [IsAuthenticated]

class GameDetailView(APIView):
    def get(self, request, tournament, slug):
        game = get_object_or_404(Game, slug=slug)
        serializer = GameDetailSerializer(game)
        return Response(serializer.data)