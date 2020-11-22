from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms

# from django.template import loader
from blogging.models import Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import BaseCreateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from blogging.forms import BlogPostForm


class PostListView(ListView):
    queryset = Post.objects.exclude(published_date__exact=None).order_by(
        "-published_date"
    )
    template_name = "blogging/list.html"


class PostDetailView(DetailView):
    queryset = Post.objects.exclude(published_date__exact=None)
    template_name = "blogging/detail.html"


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
