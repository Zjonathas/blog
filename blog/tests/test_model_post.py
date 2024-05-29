from .test_post_base import PostTestBase
from blog.models import Post
from django.core.exceptions import ValidationError
from parameterized import parameterized
from django.urls import reverse
from PIL import Image
from django.conf import settings
import os


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

    def test_returns_string_representation(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_get_absolute_url_returns_url_correct(self):
        self.assertEqual(self.post.get_absolute_url(),
                         (reverse(
                             'blog:detail_post', args={self.post.pk}
                         )
                          )
                         )

    def test_resize_image(self):
        # Create a temporary image
        image_temporary = Image.new('RGB', (400, 400))
        temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg')
        image_temporary.save(temp_image_path)

        # Create a temporary image
        self.post.cover = 'temp_image.jpg'
        self.post.save()

        # Check if the cover field is not empty
        self.assertTrue(self.post.cover)

        # Remove the temporary image
        os.remove(os.path.join(settings.MEDIA_ROOT, self.post.cover.name))

    def test_resize_image_original_width_less_than_new_width(self):
        # Create a temporary image
        image_temporary = Image.new('RGB', (1920, 1080))
        temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg')
        original_height = image_temporary.height
        new_height = round((840 * original_height) / 1920)
        image_temporary.save(temp_image_path)

        # Create a temporary image
        self.post.cover = 'temp_image.jpg'
        self.post.save()

        # Check if the cover field is not empty
        self.assertEqual(self.post.cover.height, new_height)

        # Remove the temporary image
        os.remove(os.path.join(settings.MEDIA_ROOT, self.post.cover.name))

    def test_resize_image_file_not_found(self):
        self.post.cover = 'test_image/test_image_not_found.jpg'
        self.post.save()
        self.assertTrue(self.post.cover)

    def test_slug_is_generated(self):
        self.post.slug = ''
        self.post.save()
        self.assertTrue(self.post.slug)

    def test_slug_is_not_generated(self):
        self.post.slug = 'slug'
        self.post.save()
        self.assertEqual(self.post.slug, 'slug')
