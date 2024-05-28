from django.urls import resolve, reverse
from blog import views
from .test_post_base import PostTestBase
from unittest.mock import patch


class PostHomeViewTest(PostTestBase):

    def test_blog_home_view_function_is_correct(self):
        view = resolve(reverse('blog:home'))
        self.assertIs(view.func.view_class, views.PostListViewHome)

    def test_blog_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)

    def test_blog_home_template_load_is_correct(self):
        response = self.client.get(reverse('blog:home'))
        self.assertTemplateUsed(response, 'blog/page/home.html')

    def test_blog_home_template_shows_no_posts_found_if_no_recipes(self):
        response = self.client.get(reverse('blog:home'))
        self.assertContains(response, 'No posts found')

    def test_blog_home_template_load_posts(self):
        self.make_post()
        reponse = self.client.get(reverse('blog:home'))
        content = reponse.content.decode('utf-8')
        self.assertIn('Test', content)

    def test_blog_home_template_dont_load_not_published(self):
        self.make_post(is_published=False)
        response = self.client.get(reverse('blog:home'))
        self.assertIn(
            'No posts found',
            response.content.decode('utf-8')
        )

    @patch('blog.views.listview_post.PER_PAGE', new=11)
    def test_blog_home_is_paginated(self):
        wanted_number_posts = 11
        self.make_post_in_bath(wanted_number_posts)
        response = self.client.get(reverse('blog:home'))
        qtd_of_posts_in_page = len(response.context.get('posts'))

        self.assertEqual(qtd_of_posts_in_page, wanted_number_posts)

    @patch('blog.views.listview_post.PER_PAGE', new=11)
    def test_invalid_page_query_uses_first_page(self):
        self.make_post_in_bath(11)
        response = self.client.get(reverse('blog:home'), {'page': 2})
        self.assertEqual(response.context['posts'].number, 1)
