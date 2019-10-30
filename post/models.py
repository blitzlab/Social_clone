from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
# import misaka
from group.models import Group
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name = 'post', on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    text = models.TextField()
    text_html = models.TextField(editable = False)
    create_date = models.DateTimeField(auto_now = True)
    group = models.ForeignKey(Group, related_name = 'post', null = True, blank = 'True', on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        # self.text_html = self.text #)misaka.html(
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post:single', kwargs={'username':self.user.username,'pk':self.pk})

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-create_date']
        unique_together = ['user', 'text']
