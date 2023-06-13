from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class UserPostModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(UserPostModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.owner} and {self.slug}'