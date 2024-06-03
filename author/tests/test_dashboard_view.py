from django.urls import reverse, resolve
from blog.tests.test_post_base import PostTestBase
from author.views.dashboard_post import DashboardPost
from django.test import TestCase
from django.contrib.auth.models import User


class AuthorLoginRequiredTest(PostTestBase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        User.objects.create_user(username='test_login', password='test')
        self.client.login(username='test_login', password='test')


class DashboardPostTest(AuthorLoginRequiredTest):
    def setUp(self):
        super().setUp()
        self.post = self.make_post()

        self.url_create = reverse('author:create_post')
        self.response_create = self.client.get(self.url_create)

        self.resolved_create = resolve(self.url_create)

        self.url_edit = reverse('author:edit_post', kwargs={'id': self.post.pk}
                                )
        self.response_edit = self.client.get(self.url_edit)

        self.resolved_edit = resolve(self.url_edit)

    def test_dashboard_create_post_uses_correct_view(self):
        self.assertIs(self.resolved_create.func.view_class, DashboardPost)

    def test_dashboard_create_post_status_code(self):
        self.assertEqual(self.response_create.status_code, 200)

    def test_dashboard_edit_post_uses_correct_view(self):
        self.assertIs(self.resolved_edit.func.view_class, DashboardPost)

    def test_dashboard_edit_post_status_code(self):
        self.assertEqual(self.response_edit.status_code, 200)

    def test_dashboard_edit_post_load_correct_template(self):
        self.assertTemplateUsed(self.response_edit,
                                'author/page/dashboard_post.html')

    def test_dashboard_create_post_load_correct_template(self):
        self.assertTemplateUsed(self.response_create,
                                'author/page/dashboard_post.html')
