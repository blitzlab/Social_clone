from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from .models import Group, GroupMember
from django.urls import reverse
from django.views import generic
from django.urls import reverse

# Create your views here.
class CreateGroup(LoginRequiredMixin, generic.CreateView):
    model = Group
    fields = ('name', 'description')


class SingleGroup(generic.DetailView):
    model = Group

class ListGroup(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('group:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        user = self.request.user

        try:
            GroupMember.objects.create(user=user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'Warning, already a member!')
        else:
            messages.success(self.request, 'You are now a member!')

        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('group:single', kwargs={'slug':self.kwargs.get('slug')})


    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
            user=self.request.user,
            group__slug=self.kwargs.get('slug')
            ).get()

        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'You are not a member of this group!')

        else:
            membership.delete()
            messages.success(self.request, 'You have left the group!')
        return super().get(request, *args, **kwargs)
