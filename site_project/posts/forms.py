from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Post, User


BAD_WORDS = (
    'блять', 'бля', 'сука', 'пиздец', 'пизда', 'жопа', 'говно', 'хуй',
)
WARNING = 'Не ругайтесь!'


class UserForm(forms.ModelForm):
    '''Модель формы для пользователя.'''
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class PostForm(forms.ModelForm):
    '''Модель формы для поста.'''
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        """Не позволяем ругаться в отправляемом посте."""
        text = self.cleaned_data['text']
        lowered_text = text.lower()
        for word in BAD_WORDS:
            if word in lowered_text:
                raise ValidationError(WARNING)


class CommentForm(forms.ModelForm):
    '''Модель формы для комментария.'''
    class Meta:
        model = Comment
        fields = ('text',)

    def clean(self):
        """Не позволяем ругаться в комментариях."""
        text = self.cleaned_data['text']
        lowered_text = text.lower()
        for word in BAD_WORDS:
            if word in lowered_text:
                raise ValidationError(WARNING)
