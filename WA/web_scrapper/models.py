from django.db import models
from django.contrib.auth import get_user_model

class URLS(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="urls", on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=10000)

class Tag(models.Model):
    user = models.ForeignKey(URLS, related_name="tags", on_delete=models.CASCADE, null=True)
    element = models.CharField(max_length=255)
    attribute = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
