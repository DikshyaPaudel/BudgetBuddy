from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
 amount=models.FloatField()
 date=models.DateField(default=now)
 description = models.TextField()
 owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
 category=models.CharField(max_length=400, blank=True, null=True, default=None)

 def __str__(self):
  return self.category
 
 class Meta:
  ordering= ['-date']
 
class Category(models.Model):
  name=models.CharField(max_length=400)

  def save(self, *args, **kwargs):
        self.name = self.name.upper()  
        super().save(*args, **kwargs)

  class Meta:
     verbose_name ='Category'
     verbose_name_plural='Categories'

  def __str__(self):
     return self.name
 
