from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from django_quill.fields import QuillField
from taggit.managers import TaggableManager

# Create your models here.
class Category(models.Model):
    ''' A model for all the different types of categories'''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    '''Model for the post/article '''
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # slug = models.SlugField(null=True, blank=True, max_length=100)
    tags = TaggableManager()
    category = models.CharField(max_length=100, default="Default")
    content = QuillField()
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name="article_posts")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})