from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import User, Post
from . import forms
from django.http import Http404
from django.contrib import messages
from braces.views import SelectRelatedMixin
# Create your views here.
User = User
class PostList(SelectRelatedMixin, generic.ListView):
    model = Post
    select_related = ['user', 'group']

class UserPosts(generic.ListView):
    model = Post
    template_name = 'post/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('post').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.post.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = Post
    select_related = ['user', 'group']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('title', 'text', 'group')
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):

    model = Post
    select_related = ['user', 'group']
    success_url = reverse_lazy('post:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
