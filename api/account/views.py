from django.shortcuts import render
from django.http import Http404
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# Create your views here.

from .models import User
from .serializers import UserSerializer, LoginSerializer

class HelloWorldAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        return Response({"msg":"Hello-World"})
    
class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response({
            'token': user.tokens(),
            'user':{
                'id': user.id,
                'email': user.email,
                'fName': user.fname,
                'lName': user.lname
            }
        })



class UserSignUpAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'token': user.tokens(),
            'user':UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
    
class UserUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        id = self.kwargs.get('id')
        user = User.objects.filter(id=id).first()
        if user is None:
            raise Http404("User not found.")
        return user
    