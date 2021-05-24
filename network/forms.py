from django import forms
from django.core.exceptions import ValidationError
from .models import User, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

        labels = {
            'content': ""
        }