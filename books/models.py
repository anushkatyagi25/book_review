from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import *

# Create your models here.
class UserType(models.TextChoices):
    NORMAL='NORMAL','normal'
    ADMIN='ADMIN','admin'

class CustomUser(AbstractUser):
    type=models.CharField(max_length=20, choices=UserType.choices,default=UserType.NORMAL)
    def __str__(self):
        return f"{self.first_name} {self.last_name}  {self.type}"


class Book(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    genre=models.CharField(max_length=100)
    description=models.TextField()
    def average_rating(self):
        avg_rating=self.reviews.aggregate(avg=Avg('rating'))['avg']
        avg_rating=round(avg_rating,1)
        if avg_rating is not None:
            return avg_rating 
        else:
            return 0
        
class Review(models.Model):
    book=models.ForeignKey(Book,related_name="reviews",on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    comment=models.TextField()
    rating=models.IntegerField()

