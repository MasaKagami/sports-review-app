from django.urls import path
from .views import CreateUserView, UserDetailView, DeleteUserView, UpdateUserView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='user-register'),
    path('account/', UserDetailView.as_view(), name='user-detail'),
    path('account/update/', UpdateUserView.as_view(), name='user-update'),
    path('account/delete/', DeleteUserView.as_view(), name='user-delete'),
]
