from django.db import models

# Create your models here.

from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='posts', null=True, blank=True)
    title = models.CharField(max_length=100)
    caption = models.TextField(default='기본 캡션')
    created_at = models.DateTimeField(default=timezone.now)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='posts/')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)  # 좋아요 누른 유저들


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # 로그인 유저(없을 수 있음)
    nickname = models.CharField(max_length=30, null=True, blank=True)  # 비로그인 랜덤 닉네임
    content = models.TextField()
    like_count = models.IntegerField(default=0)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
