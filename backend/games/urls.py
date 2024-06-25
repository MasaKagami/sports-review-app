from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, GameDetailView

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='games')

urlpatterns = [
    path('', include(router.urls)),
    path('<slug:tournament>/<slug:slug>/', GameDetailView.as_view(), name='game-detail'),
]