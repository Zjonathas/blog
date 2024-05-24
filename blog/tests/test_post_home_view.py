from django.urls import resolve, reverse
from blog import views
from test_post_base import PostTestBase


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
