from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewListCreateView, ReviewDetailView

router = DefaultRouter()
router.register(r'reviews', ReviewListCreateView, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('<str:username>/<slug:tournament>/<slug:slug>/', ReviewDetailView.as_view(), name='user-review'),
]
