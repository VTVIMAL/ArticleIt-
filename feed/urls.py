from django.urls import path

from .views import HomePage, PostDetail, CreatePost, PostUpdate, PostDelete


urlpatterns = [
    path("<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("<int:pk>/edit/", PostUpdate.as_view(), name="post-edit"),
    path("<int:pk>/delete/", PostDelete.as_view(), name="post-delete"),
    path("create/", CreatePost.as_view(), name="create"),
    path("", HomePage.as_view(), name="home"),
]