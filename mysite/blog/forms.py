from django import forms
from .models import Comment


# комментирование постов
class CommentForm(forms.ModelForm):
    class Meta:
        # для какой модели использую форму
        model = Comment
        # какие поля использовать в форме (по умолчанию исп все)
        # fields = ['name', 'email', 'body']
        
        # комментирование без Emaila
        # fields = ['name', 'body']
        # без Email, замена name на Имя
        fields = ['Имя', 'Комментарий']


# Форма представления для поиска постов
class SearchForm(forms.Form):
    query = forms.CharField()

