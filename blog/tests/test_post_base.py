from django.test import TestCase
from blog.models import Post, User


class PostMixin:
    def make_author(
            self,
            username='test12121221122',
            first_name='Test12',
            last_name='Test12',
            password='test12',
            email='teste12',
            ):
        return User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )

    def make_post(
            self,
            title='Test',
            content='Test',
            description='Test',
            author_data=None,
            slug='test-test-test-test',
            is_published=True,
            ):
        if author_data is None:
            author_data = {}
        return Post.objects.create(
            title=title,
            content=content,
            description=description,
            author=self.make_author(**author_data),
            slug=slug,
            is_published=is_published,
        )

    def make_post_in_bath(self, qty=10):
        """
        Make multiple posts

        :param qtd: int

        qtd = quantity
        """
        posts = []
        for _ in range(qty):
            kwargs = {
                'title': f'Post title {_}',
                'slug': f'post-title-{_}',
                'author_data': {'username': f'u{_}'},
            }
            post = self.make_post(**kwargs)
            posts.append(post)


class PostTestBase(TestCase, PostMixin):
    def setUp(self) -> None:
        return super().setUp()
