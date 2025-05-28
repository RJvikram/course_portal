from django.shortcuts import render
from instructors.serializers import InstructorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from instructors.models import Instructor
# Create your views here.

class InstructorAPIView(APIView):
    def get(self, requests, id=None,  *args, **kwargs):
        if id is not None:
            try:
                qs = Instructor.objects.get(id=id)
                serializer = InstructorSerializer(qs)
                return Response({"data" : serializer.data})
            except:
                return Response({"errors" : "Instructor id does'nt exist."})
        qs = Instructor.objects.all()
        serializer = InstructorSerializer(qs, many=True)
        return Response({"data" : serializer.data})
    
    def post(self, requests, *args, **kwargs):
        seriaalizer = InstructorSerializer(data=requests.data)
        if seriaalizer.is_valid():
            seriaalizer.save()
            return Response({"data" : seriaalizer.data})
        return Response({"errors" : seriaalizer.errors})
    def put(self, requests, id=None, *args, **kwargs):
        try:
            qs = Instructor.objects.get(id=id)
            serializer = InstructorSerializer(qs, data=requests.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data})
            return Response({"errors" : serializer.errors})
        except:
            return Response({"errors" : "Instructor id does'nt exist"})
    def patch(self, requests, *args, id=None, **kwargs):
        try:
            qs = Instructor.objects.get(id=id)
            serializer = InstructorSerializer(qs, data=requests.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data})
            return Response({"errors" : serializer.errors})
        except:
            return Response({"errors" : "Instructor id does'nt exist"})
    def delete(self, requests, id=None, *args, **kwargs):
        try:
            qs = Instructor.objects.get(id=id)
            qs.delete()
            return Response({"data" : "Instructor deleted successfully."})
        except:
            return Response({"errors" : "Instructor id does'nt exist"})