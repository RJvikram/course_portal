from django.urls import path
from accounts.views import UserAPIView, UserBasicAPIView, UserBasicDetailAPIView
urlpatterns = [
    # User APIs
    path('users/', UserAPIView.as_view(), name='user-list-create'),          # GET (list), POST (create)
    path('users/<int:id>/', UserAPIView.as_view(), name='user-detail'),      # GET, PUT, PATCH, DELETE for a single user

    # User Basic Details APIs
    path('user-basic-details/', UserBasicAPIView.as_view(), name='user-basic-list-create'),
    path('user-basic-details/<int:id>/', UserBasicDetailAPIView.as_view(), name='user-basic-detail'),
]
