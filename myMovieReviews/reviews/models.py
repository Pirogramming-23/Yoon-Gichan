from django.db import models

# Create your models here.
from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    rating = models.IntegerField()
    running_time = models.CharField(max_length=50)
    release_year = models.IntegerField()
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title