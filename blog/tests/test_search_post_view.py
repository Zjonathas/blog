from django.urls import resolve, reverse
from blog import views
from .test_post_base import PostTestBase


class SearchPostViewTest(PostTestBase):
    def setUp(self):
        super().setUp()
        self.url = reverse('blog:search')

    def test_post_search_uses_correct_view(self):
        resolved = resolve(self.url)
        self.assertIs(resolved.func.view_class, views.PostListViewSearch)

    def test_post_search_load_correct_html(self):
        response = self.client.get(self.url + '?q=test')
        self.assertTemplateUsed(response, 'blog/page/home.html')

    def test_post_search_if_no_search_term(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_post_search_if_search_term(self):
        response = self.client.get(self.url + '?q=test')
        self.assertEqual(response.status_code, 200)

    def test_post_search_if_search_term_not_found(self):
        response = self.client.get(self.url + '?q=notfound')
        self.assertContains(response, 'No posts found here')

    def test_post_search_can_find_post_by_title(self):
        title1 = 'Test Post 1'
        title2 = 'Test Post 2'

        post1 = self.make_post(title=title1,
                               slug='one',
                               author_data={'username': 'testuser1'})
        post2 = self.make_post(title=title2,
                               slug='two',
                               author_data={'username': 'testuser2'})

        response1 = self.client.get(self.url + '?q=' + title1)
        response2 = self.client.get(self.url + '?q=' + title2)
        response_both = self.client.get(self.url + '?q=Test')

        self.assertIn(post1, response1.context['posts'])
        self.assertNotIn(post2, response1.context['posts'])

        self.assertIn(post2, response2.context['posts'])
        self.assertNotIn(post1, response2.context['posts'])

        self.assertIn(post1, response_both.context['posts'])
        self.assertIn(post2, response_both.context['posts'])
