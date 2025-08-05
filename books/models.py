from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Book(models.Model):
    book_id=models.AutoField
    title=models.CharField(max_length=100)
    author_id=models.IntegerField()
    content=models.TextField()
    genre=models.CharField()
    description=models.TextField()

class UserType(models.TextChoices):
    NORMAL='NORMAL','normal'
    ADMIN='ADMIN','admin'

class customuser(AbstractUser):
    type=models.CharField(max_length=20, choices=UserType.choices,default=UserType.NORMAL)
    def __str__(self):
        return f"{{self.firstname}} {{self.lastname}}  {{self.type}}"

class Review(models.Model):
    book_id=models.ForeignKey(Book,related_name="review",on_delete=models.CASCADE)
    user=models.ForeignKey(customuser,on_delete=models.CASCADE)
    comment=models.TextField()
    rating=models.IntegerField()

