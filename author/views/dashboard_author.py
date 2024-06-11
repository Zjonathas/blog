from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from blog.models import Post
from utils.pagination import make_pagination
import os


PER_PAGE = int(os.environ.get('PER_PAGE', 9))


@method_decorator(login_required(
    login_url='blog:home', redirect_field_name='next'), name='dispatch')
class DashboardAuthorIsPublished(ListView):
    model = Post
    template_name = 'author/page/dashboard_author.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user, is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('posts'),
            PER_PAGE,
        )
        context.update(
            {
                'profile': self.request.user.username,
                'posts': page_obj,
                'page_obj': pagination_range,
            }

        )

        return context
