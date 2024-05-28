from django.urls import reverse, resolve
from blog import views
from .test_post_base import PostTestBase


class PostDetailViewTest(PostTestBase):
    def get_response(self):
        response = reverse(
                'blog:detail_post', kwargs={'pk': 1}
                )
        return response

    def test_post_detail_view_is_correct(self):
        view = resolve(self.get_response())

        self.assertIs(view.func.view_class, views.DetailPost)

    def test_post_detail_view_template_loads_the_correct_post(self):
        need_title = 'This is a detail page - It load one post'

        # Need a post for this test
        self.make_post(title=need_title)
        response = self.client.get(self.get_response())

        content = response.content.decode('utf-8')

        # Check if the title is in the content
        self.assertIn(need_title, content)

    def test_post_detail_view_template_loads_the_correct_template(self):
        # Need a post for this test
        self.make_post()
        response = self.client.get(self.get_response())

        self.assertTemplateUsed(response, 'blog/page/detail_post.html')

    def test_post_detail_view_returns_404_if_no_posts_found(self):
        response = self.client.get(self.get_response())

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_dont_load_not_published(self):
        # Need a post for this test
        self.make_post(is_published=False)
        response = self.client.get(self.get_response())

        self.assertEqual(response.status_code, 404)
