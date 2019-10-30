from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# import misaka
from django.urls import reverse
from django import template
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.



register = template.Library()

class Group(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    slug = models.SlugField(allow_unicode = True, unique = True)
    description = models.TextField(blank = True, default = '')
    description_html = models.TextField(editable = False, default = '', blank = True)
    group_icon = models.FileField(blank = True, null = True, upload_to = 'images')
    member = models.ManyToManyField(User, through ='GroupMember')
    create_date = models.DateTimeField(default = timezone.now)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = self.description#)misaka.html(
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('group:single', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name = 'membership', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name = 'user_group', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
