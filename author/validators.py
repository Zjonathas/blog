from collections import defaultdict
from django.core.exceptions import ValidationError


class AuthorPostFormValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self):
        self.clean_title()
        self.clean_content()
        self.clean_description()
        cleaned_data = self.data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self.errors['description'].append(
                'Description must be different from title'
                )

        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_title(self):
        title = self.data.get('title')
        if not title:
            self.errors['title'].append('Title is required')
            return title
        if len(title) < 5:
            self.errors['title'].append('Title must be at least 5 characters')
        return title

    def clean_content(self):
        content = self.data.get('content')
        if not content:
            self.errors['content'].append('Content is required')
            return content
        if len(content) < 10:
            self.errors['content'].append(
                'Content must be at least 10 characters'
                )
        return content

    def clean_description(self):
        description = self.data.get('description')
        if not description:
            self.errors['description'].append('Description is required')
            return description
        if len(description) < 10:
            self.errors['description'].append(
                'Description must be at least 10 characters'
                )
        return description
