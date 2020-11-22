from django.urls import path
from blogging.views import PostListView, PostDetailView
from blogging.views import add_model

urlpatterns = [
    path("", PostListView.as_view(), name="blog_index"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
    path("add/", add_model, name="add_post"),
]
