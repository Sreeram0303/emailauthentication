from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) # this will create one-one relationship with User model,parameter specifies that if the associated User instance is deleted, the corresponding user instance should also be deleted (cascading delete).
    auth_token = models.CharField(max_length=100)  #to store token
    is_verified = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# Create your models here.
