from django.db import models

# Create your models here.
class Drug(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    reason = models.TextField()
    company = models.TextField()
    rating = models.FloatField()
