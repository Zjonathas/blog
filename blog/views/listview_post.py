from django.shortcuts import render
from django.views.generic import ListView
from blog.models import Post
from utils.pagination import make_pagination
import os
from django.db.models import Q
from django.http import Http404


PER_PAGE = int(os.environ.get('PER_PAGE', 9))


class PostListViewBase(ListView):
    model = Post
    template_name = 'blog/page/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        querryset = super().get_queryset()
        querryset = querryset.filter(is_published=True)
        return querryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('posts'),
            PER_PAGE,
        )
        context.update(
            {
                'posts': page_obj,
                'page_obj': pagination_range,
            }

        )

        return context


class PostListViewHome(PostListViewBase):
    template_name = 'blog/page/home.html'


class PostListViewSearch(PostListViewBase):
    template_name = 'blog/page/home.html'

    def get_queryset(self):
        search_term = self.request.GET.get('q')
        if not search_term:
            raise Http404

        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(title__icontains=search_term) | Q(content__icontains=search_term)
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {
                'search_term': self.request.GET.get('q')
            }
        )
        return context


class PostListViewPhotos(PostListViewBase):
    template_name = 'blog/page/photos.html'
