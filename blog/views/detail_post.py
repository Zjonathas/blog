from django.views.generic import DetailView
from blog.models import Post


class DetailPost(DetailView):
    model = Post
    template_name = 'blog/page/detail_post.html'
    context_object_name = 'post'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'is_detail_page': True
        })
        return context
