from django.db import models
from courses.models import Courses
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Review(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_on = models.DateTimeField(auto_created=True)

    def __str__(self):
        return str(self.course.title + " " + self.student.first_name)
