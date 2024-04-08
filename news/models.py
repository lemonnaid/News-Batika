from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import models
from django.conf import settings


class Headline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null=True, blank=True)
    description = models.TextField(null=True)
    url = models.TextField()
    pub_date = models.DateTimeField(blank=True, null=True)
    news_source = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["username"], name="unique_username")
        ]

    def __str__(self):
        return self.username

    groups = models.ManyToManyField(
        Group,
        verbose_name=("groups"),
        blank=True,
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("user permissions"),
        blank=True,
        related_name="custom_user_set",
        related_query_name="user",
    )





class news_read(models.Model):
    user = models.CharField(max_length=100, null=True)
    articles_read = models.ManyToManyField('Headline')
    
    

    def __str__(self):
        return f"{self.user.username} - {self.articles_read.count()} articles read"


