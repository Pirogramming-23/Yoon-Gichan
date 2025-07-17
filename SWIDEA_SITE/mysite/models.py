from django.db import models
from django.contrib.auth.models import User

class DevTool(models.Model):
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=50, default='기타')
    description = models.TextField()

    def __str__(self):
        return self.name

class Idea(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE)
    image = models.FileField(upload_to='ideas/')
    interest = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class IdeaStar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'idea')

    def __str__(self):
        return f"{self.user.username} - {self.idea.name}"