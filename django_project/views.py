from rest_framework.decorators import api_view

from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework import status
#from pyjwt import token
#from rest_framework.authtoken.models import Token
from .authentication import create_access_token, create_refresh_token
from .authentication import decode_access_token, decode_refresh_token
from user.models import User
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def register(request):
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
    #    token = Token.objects.create(user=user)
        return Response({"id": serializer.data["id"], "email": serializer.data["email"]})
    
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "not found"}, status = status.HTTP_404_NOT_FOUND)
    
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    user.refresh_token = refresh_token
    user.save()
    #token, created = Token.objects.get_or_create(user=user)    #refresh token here
    serializer = UserSerializer(instance=user)
    return Response({"access_token": access_token, "refresh_token": refresh_token})

@api_view(['POST'])
def refresh(request):
    refresh_token = request.data["refresh_token"]
    token_info = decode_refresh_token(request.data["refresh_token"])
    user = User.objects.get(id=token_info["user_id"])

    if not (refresh_token == user.refresh_token):
        return Response({"detail": "wrong token"}, status = status.HTTP_404_NOT_FOUND)
    
    new_access_token = create_access_token(token_info["user_id"])
    return Response({"access_token": new_access_token})

@api_view(['POST'])
def logout(request):
    refresh_token = request.data["refresh_token"]
    token_info = decode_refresh_token(request.data["refresh_token"])
    user = User.objects.get(id=token_info["user_id"])
    
    if not (refresh_token == user.refresh_token):
        return Response({"detail": "wrong token"}, status = status.HTTP_404_NOT_FOUND)
    

    user.refresh_token = ""
    user.save()
    return Response({"success": "User logged out.", "User": user.email})

@api_view(['GET', 'PUT'])
def me(request):
    header_data = request.headers["Header"].split()

    if not (len(header_data) == 3):
        return Response({"detail": "wrong header"}, status = status.HTTP_404_NOT_FOUND)
    token = header_data[2]
    token_info = decode_access_token(token)

    if request.method == "GET":
        return Response(
            {"id": token_info["user_id"],
             "username": token_info["username"],
             "email": token_info["email"],
                }
            )
    if request.method == "PUT":
        user = User.objects.get(id=token_info["user_id"])
        user.username = request.data["username"]
        user.save()
        return Response({"username": user.username})

