from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

# from django.template import loader
from blogging.models import Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import BaseCreateView


class PostListView(ListView):
    queryset = Post.objects.exclude(published_date__exact=None).order_by(
        "-published_date"
    )
    template_name = "blogging/list.html"


class PostDetailView(DetailView):
    queryset = Post.objects.exclude(published_date__exact=None)
    template_name = "blogging/detail.html"

class PostAddView(BaseCreateView):
    queryset = Post.objects.exclude(published_date__exact=None)
    template_name = "blogging/add.html"

    # model = Poll
    # template_name = 'polling/detail.html'

    # def post(self, request, *args, **kwargs):
    #     post = self.get_object()

    #     if request.POST.get("vote") == "Yes":
    #         poll.score += 1
    #     else:
    #         poll.score -= 1
    #     poll.save()

    #     context = {"object": poll}
    #     return render(request, "polling/detail.html", context)