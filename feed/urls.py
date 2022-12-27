from django.urls import path

from .views import HomePage, PostDetail, CreatePost, PostUpdate, PostDelete, category_view, Explore, UserSearch, TaggedView, add_like


urlpatterns = [
    path("<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("<int:pk>/edit/", PostUpdate.as_view(), name="post-edit"),
    path("<int:pk>/delete/", PostDelete.as_view(), name="post-delete"),
    path("<int:pk>/like/", add_like, name='like-post'),
    path("category/<str:cat>/", category_view, name='category'),
    path('explore/', Explore.as_view(), name='explore'),
    path('search/', UserSearch.as_view(), name='profile-search'),
    path('tag/<str:tag>/', TaggedView.as_view(), name='tagged-posts'),
    path("create/", CreatePost.as_view(), name="create"),
    path("", HomePage.as_view(), name="home"),
]