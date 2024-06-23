from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, ReviewListCreateView, LikeView
from .views import GameDetailView, ReviewDetailView


# Create a router and register your viewsets with it.
router = DefaultRouter()
router.register(r'games', GameViewSet, basename='games')
router.register(r'reviews', ReviewListCreateView, basename='reviews')
router.register(r'likes', LikeView, basename='likes')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('<slug:tournament>/<slug:slug>/', GameDetailView.as_view(), name='game-detail'),
    path('<str:username>/<slug:tournament>/<slug:slug>/', ReviewDetailView.as_view(), name='user-review'),
]