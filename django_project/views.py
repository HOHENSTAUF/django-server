from rest_framework.decorators import api_view

from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework import status
#from pyjwt import token
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def register(request):
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "not found"}, status = status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)    #refresh token here
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def refresh(request):
    return Response({})

@api_view(['POST'])
def logout(request):
    
    return Response({})

@api_view(['GET', 'PUT'])
def me(request):
    return Response({})

'''
@api_view(['PUT'])
def me(request):
    return Response({})
'''