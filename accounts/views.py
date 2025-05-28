from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializers, UserBasicSerializers
from accounts.mixins import PaginationHandlerMixin
from accounts.models import UserBasicDetails
User = get_user_model()
# Create your views here.

class UserAPIView(APIView, PaginationHandlerMixin):
    def get(self, request, id=None,  *args, **Kwargs):
        if id is not None:
            try:
                qs = User.objects.get(id=id)
            except:
                return Response({"errors" : "Provided user id does'nt avileble."})
            serializer = UserSerializers(qs)
        else:
            users = User.objects.all().order_by("-id")
            paginator, page = self.paginate_queryset(users, request)
            if page is not None:
                serializer = UserSerializers(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            serializer = UserSerializers(users, many=True)       
        return Response(serializer.data)
    
    def post(self, request, *args, **Kwargs):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data})
        return Response({"errors" : serializer.errors})
    
    def put(self, request, id=None, *args, **Kwargs):
        qs = User.objects.get(id=id)
        serializer = UserSerializers(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data})
        return Response({"errors" : serializer.errors})
    
    def patch(self, request, id=None, *args, **Kwargs):
        qs = User.objects.get(id=id)
        serializer = UserSerializers(qs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data})
        return Response({"errors" : serializer.errors})
    
    def delete(self, request, id=None, *args, **Kwargs):
        try:
            qs = User.objects.get(id=id)
            qs.delete()
        except:
            return Response({"errors" : "Provided user id does'nt avileble."})
        return Response({"message" : "Data deleted sucessfully"})
    
class UserBasicAPIView(ListCreateAPIView):
    queryset = UserBasicDetails.objects.all().order_by("-id")
    serializer_class = UserBasicSerializers

class UserBasicDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserBasicDetails.objects.all().order_by("-id")
    serializer_class = UserBasicSerializers
    lookup_field = "id"
