from django.db import models
from django.db.models import ForeignKey


# Create your models here.
class TGUsers(models.Model):
    user_id = models.CharField(max_length=100)


class Tags(models.Model):
    name = models.CharField(max_length=100)

class UserTask(models.Model):
    user = ForeignKey(TGUsers, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=300)
    datetime = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tags)