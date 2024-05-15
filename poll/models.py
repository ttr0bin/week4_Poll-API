from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    agree = models.IntegerField(default=0)
    disagree = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
