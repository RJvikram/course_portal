from django.db import models
from courses.models import Courses
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Enrollment (models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_created=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student.first_name + " " + self.course.title)
