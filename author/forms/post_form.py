from django import forms
from collections import defaultdict
from blog.models import Post
from utils.django_forms import add_attr
from author.validators import AuthorPostFormValidator


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.my_errors = defaultdict(list)

        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Post
        fields = ['title', 'content', 'description', 'cover']

        widgets = {
            'cover': forms.FileInput(attrs={'class': 'span2'}),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorPostFormValidator(self.cleaned_data, ErrorClass=self.my_errors)
        return super_clean
