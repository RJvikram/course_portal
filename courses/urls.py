from django.urls import path
from courses.views import CoursesAPIView
urlpatterns = [
    path("course/", CoursesAPIView.as_view(), name="courses"),
    path("course/<int:id>/", CoursesAPIView.as_view(), name="courses")
]