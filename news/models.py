
from django.db import models
class Headline(models.Model):
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  description = models.TextField(null=True)
  url = models.TextField()
  pub_date = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return self.title
  
  
class register(models.Model):
  firstname = models.CharField(max_length=250)
  secondname = models.CharField(max_length=250)
  username =  models.CharField(max_length=250)
  password1 = models.CharField(max_length=250)
  password2 = models.CharField(max_length=250)
  