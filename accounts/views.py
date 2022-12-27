from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from feed.models import Post
from .models import Profile, CustomUser
from .forms import UserInfoForm, UserForm

# Create your views here.
class ProfileView(View):
    '''User Profile containing all the users article posts and an option to follow that user'''
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        user = profile.user
        user_posts = Post.objects.filter(author= user).order_by('-date_created')
        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False
                
        if request.user in followers:
            is_following = True
        else:
            is_following = False

        num_of_followers = len(followers)

        context = {
            'user':user, 
            'profile':profile, 
            'user_posts':user_posts,
            'num_of_followers': num_of_followers,
            'is_following': is_following,
            }
        return render(request, 'profile.html', context)

class UpdateProfileInfo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''Used to update the profile info such as bio and profile pic '''
    template_name = "profile_edit.html"
    model = Profile
    form_class = UserInfoForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user:
            return True
        return False
    
class UpdateUserInfo(LoginRequiredMixin,UpdateView):
    ''' View to update the user information like username and email '''
    model = CustomUser
    form_class = UserForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

class AddFollower(LoginRequiredMixin, View):
    ''' Gives the fuctionality to follow a profile so that you can stay updated about their posts'''
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)
        return redirect('profile', pk=profile.pk)

    
class RemoveFollower(LoginRequiredMixin, View):
    ''' Functionality to unfollow an user profile such that you can no longer view their posts in you personalized feed'''
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        return redirect('profile', pk=profile.pk)