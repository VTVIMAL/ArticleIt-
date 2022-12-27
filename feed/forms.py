from django import forms

from .models import Post, Category
from taggit.forms import TagWidget

choices = Category.objects.all().values_list("name", "name")

choice_list = []

for item in choices:
    choice_list.append(item)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "tags", "category", "content", )

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'tags' : TagWidget(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "tags", "category", "content", )

        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "tags": TagWidget(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            "content": forms.Textarea(attrs={'class': 'form-control'}),
        }