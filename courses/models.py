from django.db import models
from instructors.models import Instructor
# Create your models here.

class Courses(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.title
