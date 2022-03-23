from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.urls import reverse
# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated = models.DateTimeField(default=timezone.now)
    blog_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # comment_title = models.CharField(max_length=200)
    comment_text = models.TextField()
    comment_updated = models.DateTimeField(default=timezone.now)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comment_title
