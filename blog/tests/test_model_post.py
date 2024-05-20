from test_post_base import PostTestBase
from blog.models import Post
from django.core.exceptions import ValidationError
from parameterized import parameterized


class PostModelTest(PostTestBase):
    def setUp(self) -> None:
        self.post = self.make_post()
        return super().setUp()

    def make_post_no_default(self, **kwargs):
        post = Post(
            author=self.make_author(username='Test Default Author'),
            title='Post Title Default 1',
            content='Post Content Default 1',
            description='Post Description Default 1',
            slug='post-title-default-1',
            is_published=True,
        )

        post.full_clean()
        post.save()

        return post

    @parameterized.expand([
        ('title', 150),
        ('description', 300),
        ]
        )
    def test_post_fields_max_length(self, field, max_length):
        setattr(self.post, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.post.full_clean()
