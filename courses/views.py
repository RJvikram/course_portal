from django.shortcuts import render
from rest_framework.views import APIView
from courses.models import Courses
from courses.serializers import CoursesSerializers
from rest_framework.response import Response
from django.db.models import Count, Avg
from instructors.models import Instructor
# Create your views here.

class CoursesAPIView(APIView):
    def get(self, requests, id=None, *args, **kwargs):
        # Q1.  Get the total number of courses in the system.
        qs = Courses.objects.all().count()
        print(qs)
        
        if id is not None:
            qs = Courses.objects.get(id=id)
            serializer = CoursesSerializers(qs)
            return Response(serializer.data)
        qs = Courses.objects.all().order_by("-id")
        serializer = CoursesSerializers(qs, many=True)
        return Response(serializer.data)
            
    def post(self, requests, *args, **kwargs):
        serializer = CoursesSerializers(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, requests, id=None, *args, **kwargs):
        qs = Courses.objects.get(id=id)
        serializer = CoursesSerializers(qs, data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self, requests, id=None, *args, **kwargs):
        qs = Courses.objects.get(id=id)
        serializer = CoursesSerializers(qs, data=requests.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, requests, id=None, *args, **kwargs):
        if id is not None:
            qs = Courses.objects.get(id=id)
            qs.delete()
            return Response({"data" : "data delete successfully"})
        return Response({"error" : "data is not provided"})
  