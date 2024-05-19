from django.shortcuts import render
from django.views.generic import ListView
from blog.models import Post


class PostListViewBase(ListView):
    model = Post
    template_name = 'blog/page/home.html'
    context_object_name = 'posts'
    paginate_by = 9
    ordering = ['-created_at']

    def get_queryset(self):
        querryset = super().get_queryset()
        querryset = querryset.filter(is_published=True)
        return querryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(context.get('posts'))
        return {'posts': context.get('posts')}


class PostListViewHome(PostListViewBase):
    template_name = 'blog/page/home.html'
