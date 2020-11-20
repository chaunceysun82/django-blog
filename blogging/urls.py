from django.urls import path
from blogging.views import PostListView, PostDetailView, PostAddView

urlpatterns = [
    path("", PostListView.as_view(), name="blog_index"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="blog_detail"),
    path("add/", PostAddView.as_view(), name="add_post")
]
