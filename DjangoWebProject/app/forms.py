"""
Definition of forms.
"""

from django.db import models
from.models import Comment, Product
from.models import Blog

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class FeedbackForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    email = forms.EmailField(label='Ваша электронная почта', min_length=7)
    gender = forms.ChoiceField(label='Ваш пол', choices=[('1', 'Мужской'), ('2', 'Женский'), ('3', 'Другое')], widget=forms.RadioSelect, initial=3)
    hasPhone = forms.BooleanField(label='Пользуетесь ли вы продукцией Xiaomi?', required=False)
    rating = forms.ChoiceField(label='Как бы вы оценили наш сайт?', choices=[('1', 'Плохо'), ('2', 'Нормально'), ('3', 'Хорошо'), ('4', 'Отлично'), ('5', 'Превосходно')])
    comment = forms.CharField(label='Ваш комментарий', widget=forms.Textarea(attrs={'rows':12,'cols':20}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        lables = {'text': 'Комментарий'}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {
            'title': "Заголовок",
            'description': "Краткое содержаение",
            'content': "Полное содержание",
            'image': "Картинка"
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'content', 'image', 'price', 'category',)
        labels = {
            'name': "Название продукта",
            'description': "Краткое описание",
            'content': "Полное описание",
            'image': "Путь к картинке",
            'price': "Цена",
            'category': "Категория"
        }
