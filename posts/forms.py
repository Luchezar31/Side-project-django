from django import forms
from django.core.exceptions import ValidationError

from posts.mixins import ReadOnlyMixin
from posts.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'language': forms.RadioSelect(
                attrs={
                    'class': 'radio-select'
                }
            )
        }
        error_messages = {
            'author': {
                'max_length': 'Hey that is too long'
            }
        }

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title in content:
            raise ValidationError(
                'It is not a good practice to include the title in a content!'
            )
        return cleaned_data

    def save(self, commit=True):
        post = super().save(commit=False)

        post.author = post.author.capitalize()

        if commit:
            post.save()
        return post


class PostCreateForm(PostBaseForm):
    pass


class PostEditForm(PostBaseForm):
    pass


class PostDeleteForm(ReadOnlyMixin,PostBaseForm):
    pass


class SearchBarForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search for posts...'},
        )
    )
