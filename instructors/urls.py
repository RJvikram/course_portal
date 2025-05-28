from django.urls import path
from instructors.views import InstructorAPIView
urlpatterns = [
    path('instructor/', InstructorAPIView.as_view(), name="instructor"),
    path('instructor/<int:id>/', InstructorAPIView.as_view(), name="instructor-details")
]