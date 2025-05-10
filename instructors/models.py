from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.first_name