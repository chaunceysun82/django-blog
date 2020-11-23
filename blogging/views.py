from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms

# from django.template import loader
from blogging.models import Post, Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from blogging.serializers import UserSerializer, GroupSerializer
from blogging.serializers import PostSerializer, CategorySerializer
from blogging.forms import BlogPostForm


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows blog posts to be viewed or edited.
    """
    queryset = Post.objects.order_by("-published_date").exclude(
        published_date__exact=None
    )
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class PostListView(ListView):
    template_name = "blogging/list.html"
    queryset = Post.objects.exclude(published_date__exact=None).order_by(
        "-published_date"
    )


class PostDetailView(DetailView):
    template_name = "blogging/detail.html"
    queryset = Post.objects.exclude(published_date__exact=None)


@login_required
def add_model(request):

    if request.method == "POST":
        form = BlogPostForm(request.POST or {})

        if form.is_valid():

            model_instance = form.save(commit=False)
            model_instance.author = request.user
            model_instance.title = request.POST.get("title")
            model_instance.text = request.POST.get("text")
            model_instance.published_date = timezone.now()
            model_instance.save()
            return HttpResponseRedirect("/")

        else:
            return render(request, "blogging/add.html", {"form": form})
    else:
        form = BlogPostForm()

        return render(request, "blogging/add.html", {"form": form})
