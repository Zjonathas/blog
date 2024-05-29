from utils.pagination import make_pagination
from django.urls import reverse
from blog.models import Post
from blog.tests.test_post_base import PostTestBase


class MakePaginationTest(PostTestBase):
    def test_make_pagination_returns_current_page_correct(self):
        # Need a post for this test
        self.make_post()
        response = self.client.get(reverse('blog:home'))

        pag_obj, pagination_range = make_pagination(
            request=response.wsgi_request,
            queryset=Post.objects.all().order_by('-created_at'),
            per_page=1,
            qty_pages=4,
        )

        self.assertEqual(pag_obj.number, 1)

    def test_make_pagination_current_page_invalid_returns_first_page(self):
        # Need a post for this test
        self.make_post()
        response = self.client.get(reverse('blog:home'))
        response.wsgi_request.GET = {'page': 'invalid'}
        pag_obj, pagination_range = make_pagination(
            request=response.wsgi_request,
            queryset=Post.objects.all().order_by('-created_at'),
            per_page=1,
            qty_pages=4,
        )

        self.assertEqual(pag_obj.number, 1)
