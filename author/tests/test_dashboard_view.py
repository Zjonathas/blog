from django.urls import reverse, resolve
from blog.tests.test_post_base import PostTestBase
from author.views.dashboard_post import DashboardPost
from django.test import TestCase
from django.contrib.auth.models import User


class AuthorLoginRequiredTest(PostTestBase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        if User.objects.filter(username='test_login1').exists():
            User.objects.get(username='test_login1').delete()
        self.user = User.objects.create_user(username='test_login1', password='test')
        self.client.login(username='test_login1', password='test')


class DashboardPostTest(AuthorLoginRequiredTest):
    def setUp(self):
        super().setUp()
        self.post = self.make_post()

        self.url_create = reverse('author:create_post')
        self.response_create = self.client.get(self.url_create)

        self.resolved_create = resolve(self.url_create)

        self.url_edit = reverse('author:edit_post', kwargs={'id': self.post.pk}
                                )
        self.response_edit = self.client.get(self.url_edit, follow=True)

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

    def test_dashboard_edit_post_has_form(self):
        form = self.response_edit.context.get('form')
        self.assertIsNotNone(form)

    def test_dashboard_create_post_has_form(self):
        form = self.response_create.context.get('form')
        self.assertIsNotNone(form)

    def test_dashboard_edit_post_form_data_valid(self):
        # Delete user created before
        self.user.delete()

        # Create new post and new user
        self.post = self.make_post(
            author_data={'username': 'test_login2', 'password': 'test'},
            title='Test12',
            content='Test12',
            description='Test12',
            slug='test-test-test-test12',
            is_published=True,

        )

        # Login with new user
        self.client.login(username='test_login2', password='test')

        # Edit post
        response = self.client.post(reverse('author:edit_post', kwargs={
                'id': self.post.pk
                }
                ),
                data={
                'title': 'New title',
                'description': 'New description',
                'content': 'New content',
        }, follow=True)

        # Check if post was edited
        self.post.refresh_from_db()

        # Check if response is 200 and title was changed
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.title, 'New title')

    def test_dashboard_edit_post_form_data_invalid_with_data_equals(self):
        # Delete user created before

        # Create new post and new user
        self.post = self.make_post(
            author_data={'username': 'test_login3', 'password': 'test'},
            title='Test121',
            content='Test121',
            description='Test121',
            slug='test-test-test-test121',
            is_published=True,

        )

        # Login with new user

        self.client.login(username='test_login3', password='test')

        # Edit post
        response = self.client.post(reverse('author:edit_post', kwargs={
            'id': self.post.pk}),
            data={
            'title': 'a',
            'description': 'a',
            'content': 'a',
        }, follow=True)

        # Check if post was edited
        self.post.refresh_from_db()

        msg = [
            'Title must be at least 5 characters',
            'Cannot be equal to description'
            ]

        # Check if response is 200 and title was changed
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get('form').errors.get('title'), msg)

    def test_dashboard_create_post_if_dont_title(self):
        response = self.client.post(reverse('author:create_post'),
                                    data={
                                        'description': 'Test',
                                        'content': 'Test',
                                    }, follow=True)
        msg = ['Este campo é obrigatório.', 'Title is required']
        self.assertEqual(response.context.get('form').errors.get('title'), msg)

    def test_dashboard_create_post_if_title_is_less_5_characters(self):
        response = self.client.post(reverse('author:create_post'),
                                    data={
                                        'title': 'Tes',
                                        'description': 'Test',
                                        'content': 'Test',
                                    }, follow=True)
        msg = ['Title must be at least 5 characters']
        self.assertEqual(response.context.get('form').errors.get('title'), msg)

    def test_dashboard_create_post_if_dont_description(self):
        response = self.client.post(reverse('author:create_post'),
                                    data={
                                        'title': 'Test21',
                                        'content': 'Test',
                                    }, follow=True)
        msg = ['Este campo é obrigatório.', 'Description is required']
        self.assertEqual(
            response.context.get('form').errors.get('description'),
            msg
            )

    def test_dashboard_create_post_if_dont_content(self):
        response = self.client.post(reverse('author:create_post'),
                                    data={
                                        'title': 'Test21',
                                        'description': 'Test',
                                    }, follow=True)
        msg = ['Este campo é obrigatório.', 'Content is required']
        self.assertEqual(
            response.context.get('form').errors.get('content'),
            msg
            )

    def test_dashboard_create_post_if_content_is_less_10_characters(self):
        response = self.client.post(reverse('author:create_post'),
                                    data={
                                        'title': 'Test21',
                                        'description': 'Test',
                                        'content': 'Test',
                                    }, follow=True)
        msg = ['Content must be at least 10 characters']
        self.assertEqual(
            response.context.get('form').errors.get('content'),
            msg
            )
