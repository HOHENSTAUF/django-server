from rest_framework.decorators import api_view

from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework import status
#from pyjwt import token
#from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

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
    
    return Response(serializer.errors, status.HTTP_4)

@api_view(['POST'])
def login(request):
    return Response({})

@api_view(['POST'])
def refresh(request):
    return Response({})

@api_view(['POST'])
def logout(request):
    return Response({})

@api_view(['GET'])
def me(request):
    return Response({})

'''
@api_view(['PUT'])
def me(request):
    return Response({})
'''