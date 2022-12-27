from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post, Category

# Create your views here.
class HomePage(ListView):
    ''' View for the home page of the website. If a user is authenticated shows article that belongs to the profile he/she follows 
    else shows all the posts '''
    model = Post
    context_object_name = "posts"
    common_tags = Post.tags.most_common()
    category = Category.objects.all()
    template_name = "post_list.html"
    ordering = ["-date_created"]



class PostDetail(DetailView):
    '''View to show the full content of a post/article '''
    model = Post
    template_name = "post_detail.html"