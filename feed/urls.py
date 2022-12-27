from django.urls import path

from .views import HomePage, PostDetail


urlpatterns = [
    path("<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("", HomePage.as_view(), name="home"),
]