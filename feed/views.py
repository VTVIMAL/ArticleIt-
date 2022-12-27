from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Category
from .forms import PostCreateForm, PostUpdateForm

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


class CreatePost(CreateView):
    '''View for an authenticated user to create a post/article '''
    model = Post
    form_class = PostCreateForm
    template_name = "post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(UpdateView):

    '''View for the owner of the article to update/edit his post/article '''
    model = Post
    form_class = PostUpdateForm
    template_name = "post_edit.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDelete(DeleteView):
    '''View for the owner of a post to delete his post '''
    model = Post
    success_url = reverse_lazy("home")
    template_name = "post_delete.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False