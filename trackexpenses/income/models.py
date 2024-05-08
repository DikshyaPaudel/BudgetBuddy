from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Income(models.Model):
 amount=models.FloatField()
 date=models.DateField(default=now)
 description = models.TextField()
 owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
 source=models.CharField(max_length=400, blank=True, null=True, default=None)

 def __str__(self):
  return self.source
 
 class Meta:
  ordering= ['-amount']
 
class Source(models.Model):
   name=models.CharField(max_length=400)

   def save(self, *args, **kwargs):
        self.name = self.name.upper()  
        super().save(*args, **kwargs)
 
   def __str__(self):
     return self.name
 
