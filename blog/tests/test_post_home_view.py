from django.urls import resolve, reverse
from blog import views
from .test_post_base import PostTestBase
from unittest.mock import patch


class PostHomeViewTest(PostTestBase):

    def test_post_home_view_function_is_correct(self):
        view = resolve(reverse('blog:home'))
        self.assertIn(view.func.view_class, views.PostListViewHome)
