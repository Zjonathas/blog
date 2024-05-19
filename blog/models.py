from django.db import models
from django.urls import reverse
import os
from PIL import Image
from random import SystemRandom
import string
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    cover = models.ImageField(upload_to='blog/covers/%Y/%m/%d/', blank=True, default='') # noqa E501

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post", args={self.id})

    @staticmethod
    def resize_image(image, new_width=800):
        """
        Resize an image to a new width and quality is reduced to 60%
        """
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=60,
        )

    def save(self, *args, **kwargs):
        """
        If the slug is empty, it will be generated from the title
        """
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.title}-{rand_letters}')

        saved = super().save(*args, **kwargs)

        try:
            if self.cover:
                self.resize_image(self.cover, 840)
        except FileNotFoundError:
            ...

        return saved

    """def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        post_from_db = Post.objects.filter(
            title__iexact=self.title
        ).first()

        if post_from_db:
            if post_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found post with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)"""
