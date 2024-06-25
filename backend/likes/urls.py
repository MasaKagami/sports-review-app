from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LikeView

router = DefaultRouter()
router.register(r'likes', LikeView, basename='like')

urlpatterns = [
    path('', include(router.urls)),
]
