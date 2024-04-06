from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class newsCategory(models.Model):
   category_name = models.CharField(max_length=355, blank=False, null=False)

   def __str__(self):
      return self.category_name


class Headline(models.Model):
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  description = models.TextField(null=True)
  url = models.TextField()
  pub_date = models.DateTimeField(blank=True, null=True)
  news_category = models.ManyToManyField('newsCategory', blank=True)

  def __str__(self):
    return self.title
  

class intrest(models.Model):
  PreferencedNews = models.CharField(max_length=250) 


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username')
        ]

    def __str__(self):
        return self.username

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )
