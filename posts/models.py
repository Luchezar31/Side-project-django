from django.db import models

from posts.choices import LanguageChoices
from posts.validators import BadWordsValidator


class Post(models.Model):
    title = models.CharField(
        max_length=100
    )

    author = models.CharField(
        max_length=30
    )

    language = models.CharField(
        max_length=20,
        choices=LanguageChoices.choices
    )
    content = models.TextField(
        validators=[
            BadWordsValidator(bad_words=[
                'bad_word1',
                'bad_word2'
            ])
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

