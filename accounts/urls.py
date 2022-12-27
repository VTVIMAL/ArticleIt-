from django.urls import path

from .views import ProfileView, AddFollower, RemoveFollower, UpdateProfileInfo, UpdateUserInfo

urlpatterns = [
    path('profile/<int:pk>/', ProfileView.as_view(), name="profile"),
    path('update_profile/', UpdateUserInfo.as_view(), name='edit-user'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name="add-follower"),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name="remove-follower"),
    path('profile/<int:pk>/edit/', UpdateProfileInfo.as_view(), name="edit-profile"),
] 

