from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Post, Category
from .serializers import PostSerializer
from django.views.generic import TemplateView, ListView
from django.db.models import Q

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class PostAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


def home(request):
    return render(request, 'blog/home.html')


def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
    except:
        instance = get_object_or_404(Post, slug = category_slug[-1])
        return render(request, "blog/post/detail.html", {'instance':instance})
    else:
        return render(request, 'blog/post/categories.html', {'instance':instance})


def post_list(request):
    # posts = Post.published.all()
    # return render(request, 'blog/post/list.html', {'posts': posts})
    object_list = Post.published.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page })


def post_detail(request, post):
    # post = get_object_or_404(Post, slug=post, status='published')
    # return render(request, 'blog/post/detail.html', {'post':post})
    post = get_object_or_404(Post, slug=post, status='published')
    context = {}
    context['post'] = post
    context['meta'] = post.as_meta()
    return render(request, 'blog/post/detail.html', context)

#https://wsvincent.com/django-search/
class SearchResultsView(ListView, Post):
    model = Post
    template_name = 'blog/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return object_list
 