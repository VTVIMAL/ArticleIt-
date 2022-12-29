from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView , UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.db.models import Q
from django.views import View

from .models import Post, Category
from accounts.models import Profile
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

    def get_context_data(self, *args, **kwargs):
        context = super(HomePage, self).get_context_data( *args, **kwargs)
        logged_in_user = self.request.user
        common_tags = Post.tags.most_common()[:5]
        # show posts of only the users the the current user follows
        followed_posts = Post.objects.filter( author__profile__followers__in=[logged_in_user.id]).order_by('-date_created')
        category_list = Category.objects.all().order_by('name')

        context["common_tags"] = common_tags
        context['category_list'] = category_list
        context['followed_posts'] = followed_posts
        #search_filtering
        search_input = self.request.GET.get("search-box") or ''
        if search_input:
            context['followed_posts'] = context['followed_posts'].filter(title__startswith=search_input) or context['followed_posts'].filter(tags__name__startswith=search_input)
        context['search_input'] = search_input
        return context


class PostDetail(DetailView):
    '''View to show the full content of a post/article '''
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        is_liked = False
        if post.likes.filter(pk=self.request.user.pk).exists():
            is_liked =True
        context['is_liked'] = is_liked
        return context

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

def category_view(request, cat):
    # a view to show all the posts that belong to a certain category and filter them out 
    category_posts = Post.objects.filter(category=cat).order_by('-date_created')
    context = {}
    context['cat'] = cat.title()
    context['category_posts'] = category_posts
    category_list = Category.objects.all().order_by('name')
    context['category_list'] = category_list
    return render(request, 'category_post.html', context)


class Explore(LoginRequiredMixin, ListView):
    '''View for a user to explore all the latest posts without any restriction like followed posts '''
    model = Post
    template_name = 'explore.html'
    ordering = ['-date_created']


class UserSearch(LoginRequiredMixin, ListView):
    ''' Search form in the explore page so that the user can search for another user '''
    model = Profile
    template_name = 'user_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        profile_list = Profile.objects.filter(Q(user__username__icontains=search))
        list_length = profile_list.count()
        context['profile_list'] = profile_list
        context['list_length'] = list_length
        return context

class TaggedView(View):
    ''' View to show or filter by a certain tag'''
    def get(self, request, tag,  *args, **kwargs):
        tagged_posts = Post.objects.filter(tags__name=tag)
        context ={
            'tag': tag,
            'tagged_posts':tagged_posts,
        }
        return render(request, 'tagged_posts.html', context)


@login_required
def add_like(request, pk):
    # a function to add a like to the post or remove it if it was already liked
    post = get_object_or_404(Post, pk=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(pk= request.user.pk).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))